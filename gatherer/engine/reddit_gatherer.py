from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import logging

import apiconfig
from gatherer.engine.melk_format import MelkRow

SOURCE_NAME = "reddit"
POST_TYPE = "post"
COMMENT_TYPE = "comment"

USER_LIMIT = apiconfig.reddit_user_limit


def search_reddit(keyword, start_date, end_date, fields):
    """Searches Reddit archive for posts and comments related to the keyword and within date range. 

    Relies on the Pushshift project for providing access to historical Reddit posts and comments, 
    and uses the PSAW python wrapper to interact with the Pushshift API. Note that this function will only 
    return USER_LIMIT posts + comments. While there is not a cap on how many requests we can make to the 
    Pushshift API, limiting the number of posts + comments that each user can download may be helpful to 
    limit runtimes. Searching for very common terms over wide date ranges can lead to very long (multiple hours)
    runtimes if no limit is used. 

    Args: 
        keyword: string to be searched for. Currently, only one word strings are explicitly supported. 
        start_date: Datetime object representing first day of search period. 
        end_date: Datetime object representing last day of search period.
        fields: list of column headers for eventual csv database. 
    
    Returns:
        df: a Pandas Dataframe (df) containing collected information about each relevant post/comment found.
            Structured as defined in the file melk_format.py.      
    """

    api = PushshiftAPI()
    logging.basicConfig(filename="melk.log", encoding="utf-8", level=logging.DEBUG)

    # Pushshift API takes start/stop times as timestamp integers
    start = dt.datetime(start_date.year, start_date.month, start_date.day)
    start = int(start.timestamp())
    end = dt.datetime(end_date.year, end_date.month, end_date.day)
    end = int(end.timestamp())

    gen = api.search_submissions(
        q=keyword,
        limit=USER_LIMIT,
        filter=["url", "title", "subreddit", "created_utc,", "selftext"],
        after=start,
        before=end,
    )

    data = []
    posts_collected = 0
    next_id = 0

    for post in gen:
        if posts_collected % 100 == 0:

            logging.info("Downloading Reddit post #%s ....", posts_collected)

        try:
            # do not collect posts with empty bodies (includes cross posts, image/link only posts, and deleted/removed posts).
            if (
                post.selftext
                and post.selftext != "[deleted]"
                and post.selftext != "[removed]"
            ):
                collect_post(post, data, next_id)
                posts_collected += 1
                next_id += 1
        except AttributeError:
            pass

    gen = api.search_comments(
        q=keyword,
        limit=USER_LIMIT - posts_collected,
        fields=["body", "created_utc", "id", "subreddit"],
        after=start,
        before=end,
    )
    comments_collected = 0

    for comment in gen:
        if comments_collected % 100 == 0:

            logging.info("Downloading Reddit comment #%s ....", comments_collected)

        try:
            # do not collect comments with empty bodies, or deleted/removed comments
            if (
                comment.body
                and comment.body != "[deleted]"
                and comment.body != "[removed]"
            ):
                collect_comment(comment, data, next_id)
                comments_collected += 1
                next_id += 1
        except AttributeError:
            pass

    df = pd.DataFrame(data, columns=fields)

    logging.info(
        "Success! Collected %s posts and %s comments from Reddit.",
        posts_collected,
        comments_collected,
    )

    return df


def collect_post(post, data, next_id):
    """Converts information from one Reddit post into melk format, appends it as a dict to data.

    Args: 
        post: post object from generator for this post.
        data: list of collected posts/comments as dicts of MelkRow objects.  
    """
    this_post = MelkRow(
        id=next_id,
        source=SOURCE_NAME,
        full_text=post.selftext,
        type=POST_TYPE,
        title=post.title,
        section=post.subreddit,
        source_url=post.url,
        date=(dt.datetime.utcfromtimestamp(post.created_utc)),
    )

    data.append(vars(this_post))


def collect_comment(comment, data, next_id):
    """Converts information from one Reddit comment into melk format, appends it as a dict to data.

    Args: 
        comment: comment object from generator for this post. 
        data: list of collected posts/comments as dicts of MelkRow objects. 
    """
    this_comment = MelkRow(
        id=next_id,
        source=SOURCE_NAME,
        full_text=comment.body,
        type=COMMENT_TYPE,
        section=comment.subreddit,
        source_url=comment.id,  # TODO determine how to convert to accessible URL.
        date=(dt.datetime.utcfromtimestamp(comment.created_utc)),
    )
    data.append(vars(this_comment))
