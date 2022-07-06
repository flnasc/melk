# from pmaw import PushshiftAPI
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

SOURCE_NAME = "reddit"
POST_TYPE = "post"
COMMENT_TYPE = "comment"

# Placeholder: pass this in how from database?
USER_LIMIT = 10000
# USER_LIMIT = float('inf')


def search_reddit(keyword, start_date, end_date, fields):
    # takes dates as date objects. returns dataframe with collected posts in Melk format (see data).

    api = PushshiftAPI()

    start = dt.datetime(start_date.year, start_date.month, start_date.day)
    start = int(start.timestamp())
    end = dt.datetime(end_date.year, end_date.month, end_date.day)
    end = int(end.timestamp())

    # set limit = 100 for testing
    gen = api.search_submissions(
        q=keyword,
        # limit=100,
        filter=["url", "title", "subreddit", "created_utc,", "selftext"],
        after=start,
        before=end,
    )

    data = []
    posts_collected = 0
    next_id = 0

    for post in gen:
        if posts_collected % 100 == 0:
            print("Downloading post #", posts_collected, "....")
        if posts_collected > USER_LIMIT:
            break

        try:
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
        # time.sleep(0.001)
        # .001 gets backoff after 1700 posts or so
        # .01 does not get backoffs
        # time.sleep(0.1)
        # no sleep backs off after 800 posts. But, 10k posts later seems to be working ok- does psaw just handle rate limits ok?

        # Pushshift API limits to 120 requests per minute?
        # time.sleep(3)

    gen = api.search_comments(
        q=keyword,
        # limit=100,
        fields=["body", "created_utc", "id", "subreddit"],
        after=start,
        before=end,
    )
    comments_collected = 0

    for comment in gen:
        if comments_collected % 100 == 0:
            print("Downloading comment #", next_id, "....")
        if comments_collected + posts_collected > USER_LIMIT:
            break
        try:
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
    print(
        "Success! Collected ",
        posts_collected,
        " posts and ",
        comments_collected,
        " comments from Reddit.",
    )

    return df


def collect_post(post, data, next_id):
    this_post = {
        "ID": next_id,
        "SOURCE": SOURCE_NAME,
        "SECTION": post.subreddit,
        "SOURCE_URL": post.url,
        "DATE": (dt.datetime.utcfromtimestamp(post.created_utc)),
        "TITLE": post.title,
        "FULL_TEXT": post.selftext,
        "TYPE": POST_TYPE,
    }
    data.append(this_post)


def collect_comment(comment, data, next_id):
    this_comment = {
        "ID": next_id,
        "SOURCE": SOURCE_NAME,
        "SECTION": comment.subreddit,
        "SOURCE_URL": comment.id,
        "DATE": (dt.datetime.utcfromtimestamp(comment.created_utc)),
        "TITLE": "",
        "FULL_TEXT": comment.body,
        "TYPE": COMMENT_TYPE,
    }
    data.append(this_comment)


""" def test():

    start_date = dt.date.fromisoformat("2000-05-01")
    end_date = dt.date.fromisoformat("2022-06-01")
    fields = [
        "ID",
        "SOURCE",
        "SECTION",
        "SOURCE_URL",
        "DATE",
        "TITLE",
        "FULL_TEXT",
        "TYPE",
    ]
    df = search_reddit("metaverse", start_date, end_date, fields)
    print(df.head)
    print(df.tail) """



