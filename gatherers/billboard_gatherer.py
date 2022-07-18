import pandas as pd
import json
import os
import datetime as dt
from format import MelkRow
import logging

SOURCE_NAME = "billboard"
TYPE = "song"


def search_billboard(keyword, start_date, end_date, fields, path_to_dataset):
    # collects a song if it is from within the years specified (inclusive on both ends) AND the keyword appears in the lyrics

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
                        # print("Collecting ", song["title"])
                        collect_song(song, data, next_id, year)
                        next_id += 1

    df = pd.DataFrame(data, columns=fields)
    logging.info(
        "Success! Collected %s songs from Billboard Top 100 archives.", next_id
    )

    return df


def collect_song(song, data, id, year):
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
