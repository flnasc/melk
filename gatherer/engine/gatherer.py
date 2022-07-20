"""Provides main interface/manager for interacting with each source specific gatherer.

Note that apiconfig.py must be updated to use sources that require API keys- 
currently, this includes the New York Times and Twitter. That file also 
defines important configurable variables such as per user download limits and 
filepaths to local data sources, log files, and output locations.

Be aware that searches for especially common terms and/or over large date ranges may result 
in long program runtimes. To view the progress of a search, check the log file. To limit 
the maximum number of items that will be retrieved from sources with the potential to slow 
search time significantly (NYT, Reddit, and Twitter), adjust user limits in the file apiconfig.py

Also note that not every data source has data for all date ranges available, and some data sources
are not filterable by date or are only filterable by year. See the project data dictionary for 
more detailed information. 

    Typical usage example: 
        gatherer.gatherer("Seattle", "2015-01-01", "2015-02-01", "doc", ['new_york_times', 'twitter', 'reddit', 'poetry_foundation'])
"""
import pandas as pd
import datetime as dt
import logging

from gatherer.engine import nyt_gatherer
from gatherer.engine import poems_gatherer
from gatherer.engine import reddit_gatherer
from gatherer.engine import twitter_gatherer
from gatherer.engine import sotu_gatherer
from gatherer.engine import billboard_gatherer
from gatherer.engine import melk_format
import apiconfig


def gatherer(keyword, start_date, end_date, scope, sources):
    """Main interface for gatherer programs. 

    Assembles a dataset of relevant items from across specified sources, 
    then saves this dataset as a csv file. 

    Args: 
        keyword: string to be searched for. Currently expects one word alone, as a string.
        start_date: takes start date as a string in format YYYY-MM-DD (ISO 8601 standard).
            ex: June 5th, 2010 would be "2010-06-05"
        end_date: takes end date as a string in format YYYY-MM-DD, same as start date.
        scope: not implemented. Input any string. 
            TODO implement scope choice to return specific sentences or paragraphs containing keyword.
            Choose from "doc" for entire document, "paragraph", or "sentence".
        sources: list of sources to search, in any order. Choose from:
            new_york_times 
            reddit 
            poetry_foundation
            twitter
            state_of_the_union
            billboard

    Returns:
        filename_out: a string representing the name and relative location of the output csv file.

    Raises:
        ValueError: If either start or end date are improperly formatted or if the start date comes after the end date.
    """

    # validate dates: must be in proper ISO format and start date must be before end date
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

    # filemode='w' causes the log to start fresh for each run, rather than appending
    # to existing records.
    logging.basicConfig(
        filename="melk.log", filemode="w", encoding="utf-8", level=logging.INFO
    )

    for source in sources:
        if source == "new_york_times":
            logging.info("Searching New York Times Archive....")
            nyt = nyt_gatherer.search_nyt(keyword, start_date, end_date, melk_format.melk_fields)

        if source == "reddit":
            logging.info("Searching Reddit....")
            reddit = reddit_gatherer.search_reddit(keyword, start_date, end_date, melk_format.melk_fields)

        if source == "poetry_foundation":
            logging.info("Searching Poetry Foundation dataset....")
            logging.info("Warning: this dataset is NOT filterable by date.")
            poems = poems_gatherer.search_poems(keyword, melk_format.melk_fields, apiconfig.poetry_dataset_path)

        if source == "twitter":
            logging.info("Searching Twitter....")
            twitter = twitter_gatherer.search_twitter(keyword, start_date, end_date, melk_format.melk_fields)

        if source == "state_of_the_union":
            logging.info("Searching State of the Union archive")
            logging.info("Warning: this dataset is only filterable by year, not day.")
            sotu = sotu_gatherer.search_sotu(
                keyword, start_date, end_date, melk_format.melk_fields, apiconfig.sotu_dataset_path
            )

        if source == "billboard":
            logging.info("Searching Billboard Top 100 archives...")
            logging.info("Warning: this dataset is only filterable by year, not day.")
            billboard = billboard_gatherer.search_billboard(
                keyword, start_date, end_date, melk_format.melk_fields, apiconfig.billboard_dataset_path
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
    
    df.to_csv(filename_out) # save as csv file, then return name of that file
    return filename_out

