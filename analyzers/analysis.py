import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import cleaner
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords


# Input: filename/path of csv file generated by melk gatherer. Suggested to input cleaned file.
# Output: new csv file with additional columns for sentiment value
def add_sentiment_scores(csv):
    # clean data
    # clean = cleaner.main(csv)

    df = pd.read_csv(csv)

    # add column with sentiment scores initialized to zero
    df["SENTIMENT"] = 0

    df["SENTIMENT"] = [score_sentiment(text) for text in df["FULL_TEXT"]]

    # df['SENTIMENT']  = df['FULL_TEXT'].apply(lambda r : analyzer.polarity_scores(r))

    df.to_csv(csv)

    return


def score_sentiment(text):
    # Rates sentiment of text between -1 and 1, based on vader sentiment analysis
    analyzer = SentimentIntensityAnalyzer()

    sentiment_dict = {"compound": None}

    try:
        sentiment_dict = analyzer.polarity_scores(text)
    except TypeError:
        print("This text caused an error: ", text)

    return sentiment_dict["compound"]


def sentiment_histogram(csv):
    # takes csv with 'SENTIMENT' column, returns sentiment score histogram
    df = pd.read_csv(csv)
    hist = plt.hist(df["SENTIMENT"])
    plt.xlabel("Sentiment score")
    plt.ylabel("Frequency")
    # plt.show()

    return hist


def remove_stopwords(csv):
    # takes csv file of collected data, removes stopwords in place
    # stopwords come from NLTK corpus of English stopwords
    df = pd.read_csv(csv)
    df["FULL_TEXT"].dropna(inplace=True)
    df["FULL_TEXT"] = [remove_stopwords_helper(text) for text in df["FULL_TEXT"]]
    df.to_csv(csv)


def remove_stopwords_helper(text):

    out = ""

    if text == np.nan:
        print("\n****** None type*******\n")
        return text

    if text:
        try:
            stop_words = set(stopwords.words("english"))
            all_words = nltk.word_tokenize(text)
            filtered_words = [w for w in all_words if not w in stop_words]
            out = " ".join(word for word in filtered_words)
        except TypeError:
            return out

    return out
