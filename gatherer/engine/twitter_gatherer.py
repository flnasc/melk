"""Provides methods for searching Twitter Academic API. 

Note that a Twitter academic API key is required to use this module. 
Generate a bearer token and set search_tweets_bearer_token in the file 
apiconfig.py as that bearer token, expressed as a string. More here:
https://developer.twitter.com/en/products/twitter-api/academic-research

    Typical usage example: 
        twitter_data = twitter_gatherer.search_twitter(keyword, start_date, end_date, fields)
"""

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
    """Uses Twitter's API v2 Search Tweets endpoint to search for relevant Tweets. 

    Searches for Tweets related to the keyword and within the given date range. 
    Note that each Twitter Academic API access account has a monthly limit of 
    10 million Tweets per month. To help stay within this cap, search_twitter 
    will only collect USER_LIMIT tweets, where USER_LIMIT is defined as 
    twitter_user_limit within apiconfig.py.

    Args: 
        keyword: string to be searched for. Currently, only one word strings are explicitly supported. 
        start_date: Datetime object representing first day of search period. 
        end_date: Datetime object representing last day of search period.
        fields: list of column headers for eventual csv database. 
    
    Returns:
        df: a Pandas Dataframe (df) containing collected information about each relevant Tweet found.
            Structured as defined in the file melk_format.py.
    """

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

    # load_credentials() looks for credentials in environment variables, so we set those here
    os.environ["SEARCHTWEETS_ENDPOINT"] = apiconfig.search_tweets_v2_endpoint
    try:
        os.environ["SEARCHTWEETS_BEARER_TOKEN"] = apiconfig.search_tweets_bearer_token
    except TypeError:
        error = "Error. API key was not recognized in apiconfig.py. API key must be provided as a string. Ex: search_tweets_bearer_token = 'my_token'"
        logging.critical(error)
        raise TypeError(error)

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
    """Converts information from one Tweet into melk format, appends it to data as dict.

    Args:
        tweet: tweet object for the tweet being collected. 
        data: list of collected Tweets. 
        tweets_collected: int, number of Tweets collected so far. 
    """
    this_tweet = MelkRow(
        id=tweets_collected,
        source=SOURCE_NAME,
        full_text=tweet["text"],
        type=TYPE,
        source_url="https://twitter.com/twitter/status/" + tweet["id"],
        date=dt.datetime.fromisoformat(tweet["created_at"].split("Z")[0]),
    )
    data.append(vars(this_tweet))
