"""Provides various functions for analyzing datasets collected with the gatherer module. 

Does expect inputs to be in melk format as defined in gatherer/engine/melk_format.py. 

    Typical usage examples: 
        add_sentiment_scores(filename)
        remove_stopwords(filename)
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords


# Input: filename/path of csv file generated by melk gatherer. Suggested to input cleaned file.
# Output: new csv file with additional columns for sentiment value
def add_sentiment_scores(csv):
    """Adds a column with sentiment scores for each row in a dataset.

    Uses the VADER sentiment analysis package to assign a sentiment score. Records the "compound" 
    sentiment score of each item, which is expressed as a number between -1 and 1, where -1
    is the most negative and 1 is the most positive. Note that VADER was designed for use on single 
    sentences, and sentiment scores for entire documents may not be as meaningful. 
    
    Args:
        csv: string filename/path of a csv file generated by the gatherer. This csv file will be 
        modified IN PLACE: a new version of the file, with sentiment scores, is saved. 
    """

    df = pd.read_csv(csv)

    # add column with sentiment scores initialized to zero
    df["SENTIMENT"] = 0

    df["SENTIMENT"] = [score_sentiment(text) for text in df["FULL_TEXT"]]

    # df['SENTIMENT']  = df['FULL_TEXT'].apply(lambda r : analyzer.polarity_scores(r))

    df.to_csv(csv)

    return


def score_sentiment(text):
    """Helper function for add_sentiment_scores().

    Args:
        text: string, text to be analyzed. 

    Returns:
        sentiment_dict["compound"]: an integer between -1 and 1, representing the 
        overall sentiment of the text, where -1 is most negative and 1 is most positive.
    """
    
    analyzer = SentimentIntensityAnalyzer()

    sentiment_dict = {"compound": None}

    try:
        sentiment_dict = analyzer.polarity_scores(text)
    except TypeError:
        print("This text caused an error: ", text)

    return sentiment_dict["compound"]


def sentiment_histogram(csv):
    """takes csv with 'SENTIMENT' column, returns sentiment score histogram"""
    df = pd.read_csv(csv)
    hist = plt.hist(df["SENTIMENT"])
    plt.xlabel("Sentiment score")
    plt.ylabel("Frequency")
    # plt.show()

    return hist


def remove_stopwords(csv):
    """Takes csv file of collected data, removes stopwords in place"""
    df = pd.read_csv(csv)
    df["FULL_TEXT"].dropna(inplace=True)
    df["FULL_TEXT"] = [remove_stopwords_helper(text) for text in df["FULL_TEXT"]]
    df.to_csv(csv)


def remove_stopwords_helper(text):
    """Takes string of text, returns string of text containing only words that are not stop words.

    Note that this removes punctuation and whitespace as well as stopwords. 
    
    Stopwords are taken from the NLTK corpus."""

    out = ""

    if text == np.nan:
        print("\n****** None type*******\n")
        return text

    if text:
        try:
            stop_words = set(stopwords.words("english")) # Import stopwords from NLTK
            all_words = nltk.word_tokenize(text)
            filtered_words = [w for w in all_words if not w in stop_words]
            out = " ".join(word for word in filtered_words)
        except TypeError:
            return out

    return out
