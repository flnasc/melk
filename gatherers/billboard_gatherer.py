import pandas as pd
import json
import os
import datetime as dt
from format import MelkRow

SOURCE_NAME = "billboard"
TYPE = "song"


def search_billboard(keyword, start_date, end_date, fields, path_to_dataset):
    # collects a song if it is from within the years specified (inclusive on both ends) AND the keyword appears in the lyrics

    files = os.listdir(path_to_dataset)
    data = []
    next_id = 0

    for file in files:
        # expects filenames to be in format YYYY.json
        year = int(file.split(".")[0])
        if start_date.year <= year <= end_date.year:
            with open(path_to_dataset + file) as f:
                songs = json.load(f)
                for song in songs:
                    if keyword in song["lyrics"]:
                        print("Collecting ", song["title"])
                        collect_song_alt(song, data, next_id, year)
                        next_id += 1

    df = pd.DataFrame(data, columns=fields)

    return df


""" # old method
def collect_song(song, data, id, year):
    this_song = {
        "ID": id,
        "SOURCE": SOURCE_NAME,
        "SECTION": song["artist"],
        "SOURCE_URL": "",
        # puts Jan 1 as placeholder date to match format of other entries
        "DATE": str(year) + "-01-01",
        "TITLE": song["title"],
        "FULL_TEXT": song["lyrics"],
        "TYPE": TYPE,
    }
    data.append(this_song) """


def collect_song_alt(song, data, id, year):
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
