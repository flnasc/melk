import pandas as pd
import json
import os
import datetime as dt

SOURCE_NAME = "billboard"
TYPE = "song"


def search_billboard(keyword, start_date, end_date, fields, path_to_dataset):
    # collects a song if it is from within the years specified (inclusive on both ends) AND the keyword appears in the lyrics

    files = os.listdir(path_to_dataset)
    data = []
    next_id = 0

    for file in files:
        year = int(file.split(".")[0])
        if start_date.year <= year <= end_date.year:
            with open(path_to_dataset + file) as f:
                songs = json.load(f)
                for song in songs:
                    if keyword in song["lyrics"]:
                        print("Collecting ", song["title"])
                        collect_song(song, data, next_id, year)
                        next_id += 1

    df = pd.DataFrame(data, columns=fields)

    return df


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
    data.append(this_song)
