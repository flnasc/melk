"""Collects relevant song lyrics from Billboard Top 100 archive. 

Finds songs in a local dataset that contain a keyword and are within 
the specified date range. 

    Typical usage example:
        songs_data = billboard_gatherer.search_billboard(keyword, start_date, end_date, fields, path_to_dataset)
"""

import pandas as pd
import json
import os
import datetime
import logging
from gatherer.engine.melk_format import MelkRow

SOURCE_NAME = "billboard"
TYPE = "song"


def search_billboard(keyword, start_date, end_date, fields, path_to_dataset):
    """Collect songs from local dataset that contain the keyword and are within specified date range. 

    Args: 
        keyword: string to be searched for. Case sensitive, searches for exact matches. 
        start_date: Datetime object representing first day of search period (inclusive). 
        end_date: Datetime object representing last day of search period (inclusive).
        fields: list of column headers for eventual csv database. 
        path_to_dataset: location of the folder containing files for each year's Top 100 songs.
            Expects files within this folder to be named YYYY.json. Ex: 1986.json
    
    Returns:
        df: a Pandas Dataframe (df) containing collected information about each relevant song found.
            Structured as defined in the file melk_format.py.
    
    """

    files = os.listdir(path_to_dataset)
    data = []
    next_id = 0
    logging.basicConfig(filename="melk.log", encoding="utf-8", level=logging.DEBUG)

    for file in files:
        # expects filenames to be in format YYYY.json
        year = int(file.split(".")[0])
        if start_date.year <= year <= end_date.year:
            with open(path_to_dataset + file) as f:
                songs = json.load(f)
                for song in songs:
                    if keyword in song["lyrics"]:
                        logging.info("Collecting ", song["title"])
                        collect_song(song, data, next_id, year)
                        next_id += 1

    df = pd.DataFrame(data, columns=fields)
    logging.info(
        "Success! Collected %s songs from Billboard Top 100 archives.", next_id
    )

    return df


def collect_song(song, data, id, year):
    """Converts information from one song into melk format, appends it to data as a dict.

    Note that songs from a given year will be assigned a datetime of 
    YYYY-01-01 00:00:00, or Jan. 1st of that year. This is a placeholder value that ensures
    data from the Billboard archive matches the format of other sources.

    Args: 
        song: song object being collected.
        data: list of collected songs represented as dicts of MelkRow objects.
        id: the next ID number to assign.
        year: year in which this song appears in Billboard Top 100.
    """
    this_song = MelkRow(
        id=id,
        source=SOURCE_NAME,
        full_text=song["lyrics"],
        type=TYPE,
        title=song["title"],
        section=song["artist"],
        # puts Jan 1 as placeholder date to match format of other entries
        date=str(year) + "-01-01 00:00:00",
    )

    data.append(vars(this_song))
