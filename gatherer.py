from nyt_gatherer import search_nyt
from poems_gatherer import search_poems
from reddit_gatherer import search_reddit
from twitter_gatherer import search_twitter
from sotu_gatherer import search_sotu
from billboard_gatherer import search_billboard
import pandas as pd
import datetime as dt
import apiconfig

# Defining Melk format - see data dictionary for more info
FIELDS = ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"]

# driver(keyword, start_date, end_date, scope, sources)
# expects keyword as single string
# expects dates as strings in iso format [YYYY-MM-DD]
# expects sources as list of strings in any order
# Under construction: expects limit as a dict showing how many items a user can retrieve from each source:
#     example: {'new_york_times': 100, 'reddit': 2000}
#     if there is no entry for a given source, assumes no limit
# calls nyt_engine, reddit_engine, other engines
# concats into one dataframe
# then, could clean data
# could do some analysis
# save df to csv file


def driver(keyword, start_date, end_date, scope, sources):

    start_date = dt.date.fromisoformat(start_date)
    end_date = dt.date.fromisoformat(end_date)

    nyt = pd.DataFrame()
    reddit = pd.DataFrame()
    poems = pd.DataFrame()
    twitter = pd.DataFrame()
    sotu = pd.DataFrame()
    billboard = pd.DataFrame()

    for source in sources:
        if source == "new_york_times":
            print("Searching New York Times Archive....")
            nyt = search_nyt(keyword, start_date, end_date, FIELDS)

        if source == "reddit":
            print("Searching Reddit....")
            reddit = search_reddit(keyword, start_date, end_date, FIELDS)

        if source == "poetry_foundation":
            print("Searching Poetry Foundation dataset....")
            print("Warning: this dataset is NOT filterable by date.")
            poems = search_poems(keyword, FIELDS, apiconfig.poetry_dataset_path)

        if source == "twitter":
            print("Searching Twitter...")
            twitter = search_twitter(keyword, start_date, end_date, FIELDS)

        if source == "state_of_the_union":
            print("Searching State of the Union archive...")
            print("Warning: this dataset is only filterable by year, not day.")
            sotu = search_sotu(
                keyword, start_date, end_date, FIELDS, apiconfig.sotu_dataset_path
            )

        if source == "billboard":
            print("Searching Billboard Top 100 archives...")
            print("Warning: this dataset is only filterable by year, not day.")
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
