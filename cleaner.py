# accepts CSV file from melk
# saves cleaned data as a seperate file
import pandas as pd
import re


def main(filename):
    df = pd.read_csv(filename)

    # drop rows with no text
    df = df[df.FULL_TEXT.notnull()]
    df.dropna(subset=["FULL_TEXT"])
    # df = df[clean(df.FULL_TEXT)]

    # should switch to vectorized operation
    for i in range(len(df)):

        try:
            text = df.at[i, "FULL_TEXT"]
            # print("TEXT IS:      \n", text)
            text = clean(text)
            df.at[i, "FULL_TEXT"] = text
        except KeyError:
            pass

        # How are we implementing the options system?
        """if lower_flag:
                text = text.lower()
            if remove_hashtags_flag:
                text = remove_hashtags(text)
            if remove_twitter_handles_flag:
                text = remove_twitter_handles(text)"""

    #  No such file or directory: 'clean_./outputs/metaverse_2022-05-01_2022-05-02.csv'
    # filename_out = "clean_" + filename

    df.to_csv(filename)
    return filename


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


def remove_hashtags(text):
    # this removes just the # character itself:
    text = re.sub(r"#", "", text)

    # to remove the entire #phrase, use this expression:
    # text = re.sub(r"#\S+", "", text)
    return text


def remove_twitter_handles(text):
    # removes twitter handles
    text = re.sub(r"@\S+", "", text)
    return text


def test():
    # filename = "./outputs/whiskey_2022-06-20_2022-06-23.csv"
    filename = "./outputs/clean_example.csv"
    df = pd.read_csv(filename)
    print("Before cleaning, ", len(df), " rows.")
    main(filename)
    df = pd.read_csv(filename)
    print("After cleaning, ", len(df), " rows.")

    return
