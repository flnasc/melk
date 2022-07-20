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
    # takes dates as date objects. returns dataframe with collected posts in Melk format (see data).

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
            # do not collect posts with empty bodies (includes cross posts and image/link only posts and deleted/removed posts).
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
    this_comment = MelkRow(
        id=next_id,
        source=SOURCE_NAME,
        full_text=comment.body,
        type=COMMENT_TYPE,
        section=comment.subreddit,
        source_url=comment.id,
        date=(dt.datetime.utcfromtimestamp(comment.created_utc)),
    )
    data.append(vars(this_comment))
