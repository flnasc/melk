# basic tests
import pytest
import sys
import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gatherer.engine import gatherer, nyt_gatherer, reddit_gatherer, twitter_gatherer, melk_format
from analyzer.engine import analysis
from cleaner.engine import cleaner



@pytest.fixture
def url():
    return "https://www.nytimes.com/2022/05/05/sports/soccer/seattle-sounders-pumas-unam.html"


@pytest.fixture
def path_to_sounders_text():
    return "./melk/tests/sounders.txt"


"""     
@pytest.mark.api
def test_scrape_alt(url, path_to_sounders_text):
    #assert nyt_engine.scrapealt(url)
    with open(path_to_sounders_text, 'r') as file:
        data = file.read().replace('/n', '')
    assert nyt_engine.scrapealt(url) == data """


@pytest.mark.api

def test_does_the_driver_still_kinda_work():
    # run search
    filename = gatherer.gatherer(
        "whiskey",
        "2022-06-20",
        "2022-06-23",
        "doc",
        [
            "new_york_times",
            "reddit",
            "poetry_foundation",
            "twitter",
            "state_of_the_union",
            "billboard",
        ],
    )
    with open(filename, "r") as file:
        df = pd.read_csv(file)
        assert len(df) > 50


@pytest.mark.api
def test_search_reddit():
    start_date = dt.date.fromisoformat("2020-11-11")
    end_date = dt.date.fromisoformat("2021-02-03")
    df = reddit_gatherer.search_reddit(
        "loons", start_date, end_date, melk_format.melk_fields
    )
    assert len(df) > 50

@pytest.mark.current
@pytest.mark.api
def test_search_nyt():
    start_date = dt.date.fromisoformat("2009-01-01")
    end_date = dt.date.fromisoformat("2009-01-02")
    df = nyt_gatherer.search_nyt(
        "Chopin", start_date, end_date, melk_format.melk_fields
    )
    assert len(df) > 0


# @pytest.mark.fast
def test_remove_hashtags():
    assert cleaner.remove_hashtags("#hello #world") == "hello world"


# @pytest.mark.fast
def test_remove_usernames():
    assert cleaner.remove_twitter_handles("@jack") == ""
    assert (
        cleaner.remove_twitter_handles("hello @username world")
        == "hello  world"
    )

@pytest.mark.api
def test_twitter_engine():
    s = dt.date.fromisoformat("2022-05-01")
    e = dt.date.fromisoformat("2022-05-10")
    df = twitter_gatherer.search_twitter("Sounders", s, e, melk_format.melk_fields)
    assert len(df) > 50
    df.to_csv("./outputs/current.csv")


def test_billboard_engine():
    filename = gatherer.gatherer(
        "Elvis", "1960-01-01", "2022-01-02", "doc", ["billboard"]
    )
    df = pd.read_csv(filename)
    assert len(df) > 0


def test_sotu_engine():

    filename = gatherer.gatherer(
        "China", "1870-01-01", "2022-01-02", "doc", ["state_of_the_union"]
    )
    df = pd.read_csv(filename)
    assert len(df) > 0


def test_full_process_histogram():

    filename = gatherer.gatherer(
        "abortion", "2022-07-01", "2022-07-05", "doc", ["new_york_times"]
    )

    analysis.add_sentiment_scores(filename)

    df = pd.read_csv(filename)
    plt.hist(df["SENTIMENT"])
    plt.xlabel("Sentiment score")
    plt.ylabel("Frequency")
    # plt.show()


# @pytest.mark.current
def test_working_test():
    filename = gatherer.gatherer(
        "metaverse",
        "2022-05-01",
        "2022-05-02",
        "doc",
        ["twitter", "reddit", "new_york_times", "poetry_foundation"],
    )
    # filename = "./outputs/metaverse_2022-05-01_2022-05-02.csv"
    df = pd.read_csv(filename)
    # print(df.keys())
    print("\n\nOriginal length: ", len(df))
    assert len(df) > 10

    cleaner.main(filename)
    cleaner.remove_hashtags(filename)
    cleaner.remove_twitter_handles(filename)
    df = pd.read_csv(filename)
    print("Length after cleaning: ", len(df))

    analysis.remove_stopwords(filename)
    df = pd.read_csv(filename)
    print("\n\n\nAfter cleaning and removing stopwords: ", df.head(10))
    # print(df.keys())

    analysis.add_sentiment_scores(filename)
    print("\n\n\nSentiment scores added: ", df.head(10))
    analysis.sentiment_histogram(filename)

    return
@pytest.mark.api
@pytest.mark.xfail
def test_invalid_start_date():
    filename = gatherer.gatherer(
        "whiskey",
        "2",
        "2022-06-23",
        "doc",
        [
            "new_york_times",
            "reddit",
            "poetry_foundation",
            "twitter",
            "state_of_the_union",
            "billboard",
        ],
    )


@pytest.mark.xfail
def test_start_date_after_end_date():
    filename = gatherer.gatherer("whiskey",
        "2022-07-01",
        "2022-06-23",
        "doc",
        [
            "new_york_times",
            "reddit",
            "poetry_foundation",
            "twitter",
            "state_of_the_union",
            "billboard",
        ]
    )

    assert ValueError

@pytest.mark.xfail
def test_start_date_same_as_end_date():
    filename = gatherer.gatherer("whiskey",
        "2022-07-01",
        "2022-07-01",
        "doc",
        [
            "new_york_times",
            "reddit",
            "poetry_foundation",
            "twitter",
            "state_of_the_union",
            "billboard",
        ]
    )

    assert filename

