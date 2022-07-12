import os
import json
import pandas as pd
import datetime

SOURCE_NAME = "state_of_the_union"
TYPE = "speech"

def search_sotu(keyword, start_date, end_date, fields, path_to_dataset):

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
    this_speech = {
        "ID": id,
        "SOURCE": SOURCE_NAME,
        "SECTION": speech["name"],
        "SOURCE_URL": "",
        "DATE": speech["year"],
        "TITLE": "State of the Union Address " + str(speech["year"]),
        "FULL_TEXT": speech["text"],
        "TYPE": TYPE,
    }
    data.append(this_speech)
