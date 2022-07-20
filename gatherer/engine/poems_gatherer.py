"""Collects relevant poems from local dataset. 

    Typical usage example: 
        poems_data = poems_gatherer.search_poems(keyword, fields, path_to_dataset)
"""
import pandas as pd
from gatherer.engine.melk_format import MelkRow

SOURCE_NAME = "poetry_foundation"
TYPE = "poem"


def search_poems(keyword, fields, path_to_dataset):
    """Searches local dataset for poems with keyword in their body text. 

    Warning: unlike most sources, this one is NOT filterable by date. 
    Any call to search_poems will return all poems within the dataset that contain 
    the keyword (case insensitive). 

    Args:
        keyword: string to be searched for. Case insensitive, looks for exact matches otherwise.
        fields: list of column headers for eventual csv database. 
        path_to_dataset: location of the csv file containing full poetry dataset. 
            Configured in apiconfig.py
    """

    poems = pd.read_csv(path_to_dataset)

    # select poems that contain the keyword in their text. Case insensitive.
    poems = poems[poems["Poem"].str.contains(keyword, case=False)]

    df = parse_poems(poems, fields)

    return df


def parse_poems(poems, fields):
    """Creates dataframe of relevant poems in melk format, as defined in melk_format.py
    
    Args: 
        poems: dataframe of entire original poems database
        fields: list of column headers for eventual csv database.

    Returns:
        df: a Pandas Dataframe (df) containing collected information about each 
        relevant poem. 
            Structured as defined in the file melk_format.py
    """
    poems = poems.reset_index()

    data = []
    for i in range(len(poems)):
        this_poem = MelkRow(
            id=i,
            source=SOURCE_NAME,
            full_text=poems.at[i, "Poem"],
            type=TYPE,
            title=poems.at[i, "Title"],
        )
        data.append(vars(this_poem))

    df = pd.DataFrame(data, columns=fields)
    return df
