from multiprocessing.sharedctypes import Value
from gatherers.nyt_gatherer import search_nyt
from gatherers.poems_gatherer import search_poems
from gatherers.reddit_gatherer import search_reddit
from gatherers.twitter_gatherer import search_twitter
from gatherers.sotu_gatherer import search_sotu
from gatherers.billboard_gatherer import search_billboard

import pandas as pd
import datetime as dt
import apiconfig
import logging

# Defining Melk format - see data dictionary for more info
FIELDS = ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"]

# gatherer(keyword, start_date, end_date, scope, sources)
# expects keyword as single string
# expects dates as strings in iso format [YYYY-MM-DD]
#   start date must be before end date. 
# expects sources as list of strings in any order
# Under construction: expects limit as a dict showing how many items a user can retrieve from each source:
#     example: {'new_york_times': 100, 'reddit': 2000}
#     if there is no entry for a given source, assumes no limit
# calls nyt_engine, reddit_engine, other engines
# concats into one dataframe
# then, could clean data
# could do some analysis
# save df to csv file


def gatherer(keyword, start_date, end_date, scope, sources):

    # validate dates: must be in proper format and start date must be before end date
    try:
        start_date = dt.date.fromisoformat(start_date)
        end_date = dt.date.fromisoformat(end_date)
    except ValueError as error:
        logging.critical(error)
        raise ValueError(error)

    if start_date >= end_date:
        error = "Error. Start date must be before end date."
        logging.critical(error)
        raise ValueError(error)

    nyt = pd.DataFrame()
    reddit = pd.DataFrame()
    poems = pd.DataFrame()
    twitter = pd.DataFrame()
    sotu = pd.DataFrame()
    billboard = pd.DataFrame()

    # filemode='w' makes it so that log starts fresh for each run, rather than appending
    # to existing records.
    logging.basicConfig(
        filename="melk.log", filemode="w", encoding="utf-8", level=logging.INFO
    )

    for source in sources:
        if source == "new_york_times":
            # print("Searching New York Times Archive....")
            logging.info("Searching New York Times Archive....")
            nyt = search_nyt(keyword, start_date, end_date, FIELDS)

        if source == "reddit":
            # print("Searching Reddit....")
            logging.info("Searching Reddit....")
            reddit = search_reddit(keyword, start_date, end_date, FIELDS)

        if source == "poetry_foundation":
            logging.info("Searching Poetry Foundation dataset....")
            logging.info("Warning: this dataset is NOT filterable by date.")
            # print("Searching Poetry Foundation dataset....")
            # print("Warning: this dataset is NOT filterable by date.")
            poems = search_poems(keyword, FIELDS, apiconfig.poetry_dataset_path)

        if source == "twitter":
            logging.info("Searching Twitter....")
            # print("Searching Twitter...")
            twitter = search_twitter(keyword, start_date, end_date, FIELDS)

        if source == "state_of_the_union":
            logging.info("Searching State of the Union archive")
            logging.info("Warning: this dataset is only filterable by year, not day.")
            # print("Searching State of the Union archive...")
            # print("Warning: this dataset is only filterable by year, not day.")
            sotu = search_sotu(
                keyword, start_date, end_date, FIELDS, apiconfig.sotu_dataset_path
            )

        if source == "billboard":
            logging.info("Searching Billboard Top 100 archives...")
            logging.info("Warning: this dataset is only filterable by year, not day.")
            # print("Searching Billboard Top 100 archives...")
            # print("Warning: this dataset is only filterable by year, not day.")
            billboard = search_billboard(
                keyword, start_date, end_date, FIELDS, apiconfig.billboard_dataset_path
            )

    df = pd.concat([nyt, reddit, poems, twitter, sotu, billboard], ignore_index=True)
    # replace ID column with updated column that accounts for rows from other sources
    df = df.drop(columns="ID")
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": "ID"})

    filename_out = (
        apiconfig.outputs_folder_path
        + keyword
        + "_"
        + start_date.isoformat()
        + "_"
        + end_date.isoformat()
        + ".csv"
    )
    # save as csv file, then return name of that file
    df.to_csv(filename_out)
    return filename_out

