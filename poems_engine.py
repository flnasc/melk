# Poetry foundation engine
# Takes keyword, melk format fields, and path to a csv dataset of 13,000 poems scraped from
# poetryfoundation.org
# returns a pandas dataframe with collected articles in Melk format (see data dictionary).

import pandas as pd

SOURCE_NAME = "poetry_foundation"
TYPE = "poem"


def search_poems(keyword, fields, path_to_dataset):

    poems = pd.read_csv(path_to_dataset)

    # select poems that contain the keyword in their text. Case insensitive.
    poems = poems[poems["Poem"].str.contains(keyword, case=False)]

    df = parse_poems(poems, fields)

    return df


def parse_poems(poems, fields):
    # takes dataframe of poems, returns new df formatted in Melk format
    poems = poems.reset_index()

    print(poems)
    data = []
    for i in range(len(poems)):
        this_poem = {
            "ID": i,
            "SOURCE": SOURCE_NAME,
            "SECTION": "",
            "SOURCE_URL": "",
            "DATE": "",
            "TITLE": poems.at[i, "Title"],
            "FULL_TEXT": poems.at[i, "Poem"],
            "TYPE": TYPE,
        }
        data.append(this_poem)

    df = pd.DataFrame(data, columns=fields)
    return df
