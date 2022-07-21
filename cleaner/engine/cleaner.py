"""Provides text cleaning functions. Unfinished, not fully tested."""
import pandas as pd
import re


def main(filename):
    """Main cleaner function, does basic operations and manages calling optional helper functions.
    
    Args: 
        filename: name/filepath of a csv file collected by the gatherer.
    Returns:
        filename: same as input, but the cleaned file is now saved at this location."""
    df = pd.read_csv(filename)

    # drop rows with no text
    df = df[df.FULL_TEXT.notnull()]
    df.dropna(subset=["FULL_TEXT"])

    # TODO switch to vectorized operation for optimal performance on very large files
    for i in range(len(df)):

        try:
            text = df.at[i, "FULL_TEXT"]
            # print("TEXT IS:      \n", text)
            text = clean(text)
            df.at[i, "FULL_TEXT"] = text
        except KeyError:
            pass

        """How are we implementing the options system? Here is an example using flags:
        if lower_flag:
                text = text.lower()
            if remove_hashtags_flag:
                text = remove_hashtags(text)
            if remove_twitter_handles_flag:
                text = remove_twitter_handles(text)"""

    df.to_csv(filename)
    return filename


def clean(text):
    """Basic text cleaning.
    
    Removes newline characters, all occurrences of 2 or more spaces, hyperlinks, 
    and all non-word characters.
    
    Args: 
        text: string to be cleaned.
    Returns: 
        text: cleaned text. """


    # remove newlines
    text = re.sub(r"\n", " ", text)
    # remove all occurences of 2 or more spaces
    text = re.sub(r"\s{2,}", " ", text)
    # remove links
    text = re.sub(r"http\S+", "", text)
    # remove all non-word characters
    text = re.sub(r"\W+", " ", text)

    return text


def remove_hashtags(text):
    """Optional method to remove hashtags (especially useful for Twitter data).
    Note that as written it removes only the '#' character, leaving the actual text of the tag.
    E.g. '#TwitterHashtag' -> 'TwitterHashtag'.
    
    Args: 
        text: string to be cleaned.
    Returns: 
        text: cleaned text.
    """
    
    #  removes just the # character itself:
    text = re.sub(r"#", "", text)

    # to remove the entire #phrase, use this expression:
    # text = re.sub(r"#\S+", "", text)
    return text


def remove_twitter_handles(text):
    """Removes Twitter handles (usernames) from text. 

    Args: 
        text: string to be cleaned.
    Returns: 
        text: cleaned text."""

    text = re.sub(r"@\S+", "", text)
    return text
