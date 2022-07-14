import pandas as pd
import datetime as dt
import os
import apiconfig
from searchtweets import gen_request_parameters, load_credentials, collect_results

SOURCE_NAME = "twitter"
TYPE = "tweet"

# harcoded for testing
USER_LIMIT = 200


def search_twitter(keyword, start_date, end_date, fields):
    # takes dates as date objects. returns dataframe with collected tweets in Melk format
    # as defined by fields, which is taken as a list ['ID', 'SOURCE', etc.] and must match.

    query = gen_request_parameters(
        keyword + " -is:retweet",
        start_time=start_date.isoformat(),
        end_time=end_date.isoformat(),
        granularity=None,
        results_per_call=100,
        tweet_fields="id,created_at,text",
    )

    os.environ["SEARCHTWEETS_ENDPOINT"] = apiconfig.search_tweets_v2_endpoint
    os.environ["SEARCHTWEETS_BEARER_TOKEN"] = apiconfig.search_tweets_bearer_token
    search_args = load_credentials()

    results_pages = collect_results(
        query, max_tweets=USER_LIMIT, result_stream_args=search_args
    )

    data = []
    tweets_collected = 0

    for page in results_pages:
        for tweet in page["data"]:

            collect_tweet(tweet, data, tweets_collected)
            tweets_collected += 1

    df = pd.DataFrame(data, columns=fields)
    print("Success! ", tweets_collected, " tweets collected from Twitter.")

    return df


def collect_tweet(tweet, data, tweets_collected):
    this_tweet = {
        "ID": tweets_collected,
        "SOURCE": SOURCE_NAME,
        "SECTION": None,
        "SOURCE_URL": "https://twitter.com/twitter/status/" + tweet["id"],
        "DATE": dt.datetime.fromisoformat(tweet["created_at"].split("T")[0]),
        "TITLE": None,
        "FULL_TEXT": tweet["text"],
        "TYPE": TYPE,
    }
    data.append(this_tweet)
    return
