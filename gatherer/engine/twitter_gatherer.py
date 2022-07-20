import pandas as pd
import datetime as dt
import os
import logging
from searchtweets import gen_request_parameters, load_credentials, collect_results

import apiconfig
from gatherer.engine.melk_format import MelkRow

SOURCE_NAME = "twitter"
TYPE = "tweet"

USER_LIMIT = apiconfig.twitter_user_limit


def search_twitter(keyword, start_date, end_date, fields):
    # takes dates as date objects. returns dataframe with collected tweets in Melk format
    # as defined by fields, which is taken as a list ['ID', 'SOURCE', etc.] and must match.

    logging.basicConfig(filename="melk.log", encoding="utf-8", level=logging.DEBUG)

    query = gen_request_parameters(
        # does not include retweets in results
        keyword + " -is:retweet",
        start_time=start_date.isoformat(),
        end_time=end_date.isoformat(),
        granularity=None,
        results_per_call=100,
        tweet_fields="id,created_at,text",
    )

    # load_credentials looks for credentials in environment variables, so we set them here
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

    logging.info("Success! %s Tweets collected from Twitter.", tweets_collected)

    return df


def collect_tweet(tweet, data, tweets_collected):
    this_tweet = MelkRow(
        id=tweets_collected,
        source=SOURCE_NAME,
        full_text=tweet["text"],
        type=TYPE,
        source_url="https://twitter.com/twitter/status/" + tweet["id"],
        date=dt.datetime.fromisoformat(tweet["created_at"].split("Z")[0]),
    )
    data.append(vars(this_tweet))
