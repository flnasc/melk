"""Collects relevant State of the Union speeches from local dataset. 

Finds State of the Union speeches where the text contains the keyword 
and the year of the speech is within the date range given. 
Keyword search is exact and case sensitive. 

    Typical usage example: 
        sotu_data = sotu_gatherer.search_sotu(keyword, start_date, end_date, path_to_dataset)
"""

import os
import json
import pandas as pd
import datetime

from gatherer.engine.melk_format import MelkRow

SOURCE_NAME = "state_of_the_union"
TYPE = "speech"


def search_sotu(keyword, start_date, end_date, fields, path_to_dataset):
    """Searches State of the Union database for relevant speeches.

    Where text contains the keyword (exact, case-sensitive) and year of speech 
    is within given date range. Loads text and details from JSON files within 
    the folder specified by path_to_dataset. 

    Args: 
        keyword: string to be searched for. Currently, only one word strings are explicitly supported. 
        start_date: Datetime object representing first day of search period. 
        end_date: Datetime object representing last day of search period.
        fields: list of column headers for eventual csv database.
        path_to_dataset: location of the folder containing speech files. 

    Returns: 
        df: a Pandas Dataframe (df) containing collected information about each relevant speech. 
            Structured as defined in the file melk_format.py

    """
    files = os.listdir(path_to_dataset)

    data = []
    next_id = 0

    for file in files:
        with open(path_to_dataset + file) as f:
            speech = json.load(f)
            if start_date.year <= speech["year"] <= end_date.year:
                text = speech["text"]
                if keyword in text:
                    collect_speech(speech, data, next_id)
                    next_id += 1

    df = pd.DataFrame(data, columns=fields)

    return df


def collect_speech(speech, data, id):
    """Converts information from one speech into melk format, appends as dict to data.

    Note that a speech from a given year will be assigned a datetime of 
    YYYY-01-01 00:00:00, or Jan. 1st. This is a placeholder value that ensures 
    the data from speeches matches the format of data from other gatherers. 
    The only data actually available for the date of each speech is the year. 
    
    Args:
        speech: speech object from JSON file.
        data: list of collected speeches as dicts of MelkRow objects.
    """
    this_speech = MelkRow(
        id=id,
        source=SOURCE_NAME,
        full_text=speech["text"],
        type=TYPE,
        title="State of the Union Address " + str(speech["year"]),
        section=speech["name"],
        # puts Jan 1 as placeholder date to match format of other entries
        date=str(speech["year"]) + "-01-01 00:00:00",
    )
    data.append(vars(this_speech))
