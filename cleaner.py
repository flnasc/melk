# accepts CSV file from melk
# saves cleaned data as a seperate file
import pandas as pd
import re


def main(filename):
    df = pd.read_csv(filename)

    # drop rows with no text
    df = df[df.FULL_TEXT.notnull()]
    # df = df[clean(df.FULL_TEXT)]

    # should switch to vectorized operation
    for i in range(len(df)):
        text = df.at[i, "FULL_TEXT"]
        # print("TEXT IS:      \n", text)
        text = clean(text)
        df.at[i, "FULL_TEXT"] = text

    df.to_csv("./outputs/clean_example.csv")
    return df


def clean(text):

    # print(text)
    # remove newlines
    text = re.sub(r"\n", " ", text)
    # remove all occurences of 2 or more spaces
    text = re.sub(r"\s{2,}", " ", text)
    # remove links
    text = re.sub(r"http\S+", "", text)
    # remove all non-word characters
    text = re.sub(r"\W+", " ", text)

    # print(text)
    return text


def test():
    main("./outputs/metaverse_2022-05-01_2022-05-02.csv")


# test()
