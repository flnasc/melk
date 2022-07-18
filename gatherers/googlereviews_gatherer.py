from google_play_scraper import app, reviews_all, reviews
# from format import MelkRow
import datetime
import pandas as pd

class MelkRow:
    def __init__(
        self, id, source, full_text, type, title="", section="", source_url="", date=""
    ):
        self.ID = id
        self.SECTION = section
        self.SOURCE = source
        self.SOURCE_URL = source_url
        self.DATE = date
        self.TITLE = title
        self.FULL_TEXT = full_text
        self.TYPE = type

# Note: this file is unfinished, untested, and is not integrated into the main gatherer flow. 
# search_reviews_db() gives functionality similar to the other gatherers, but it relies on having a local
# database of reviews in the data folder that we do not currently provide.
#  
# Rough documentation for creating a local database of reviews from specific apps of interest: 

# collect a list of app ids from google play store URLs for each app that you want to include reviews from in the database
# ex: the app id for spotify is 'com.spotify.music', which we find in the URL: https://play.google.com/store/apps/details?id=com.spotify.music

# With this list of app IDs ['com.spotify.music', 'com.nytimes.android', etc.], call create_db(list, fields). 
#   The search_reviews_db will expect these fields to be imported from wherer they are defined in gatherer.py. 
# Once this finishes collecting data (it may take a long time for apps with many reviews), 
# it should save a csv file at ./data/google_reviews/play_store_reviews.csv

# Pass this location along with keyword and dates to search_reviews_db(). This will return a dataframe with 
# only the rows from the database we collected that match the query. 

FIELDS = ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"]
SOURCE = "google_play_store"
TYPE = "app_review"

def search_reviews_db(keyword, start_date, end_date, db_file):
    # gets reviews from local/pre-collected database. 
    # Expects this to already be in Melk format, returns a dataframe with only rows that match query. 
    # Search is case sensitive and exact- keyword must match app title precisely.   
    # TODO- implement date filtering. 

    db = pd.read_csv(db_file)
    # df = db.query('SECTION' == keyword)
    results = db[db['SECTION'] == keyword]
    # results = db[db['']]
    # print(results.head())
    # print(results.tail())
    return results 

def collect_review(review, data, id, app_id, app_title):
    this_review = MelkRow(
        id=id, 
        source=SOURCE, 
        full_text=review['content'], 
        type=TYPE, 
        section=app_title, 
        source_url="https://play.google.com/store/apps/details?id=" + app_id + "&hl=en_US&gl=US", 
        date=review['at'])
    
    data.append(vars(this_review))


# search_reviews_db("The Seattle Times", "", "", "./gatherers/data/google_reviews/play_store_reviews.csv")

def download_all_reviews(app_id, data):
    #app id example: "com.spotify.music"
    
    this_app = app(app_id)
    app_title = this_app["title"]
    print("Downloading reviews for ", app_title)
    results = reviews_all(app_id)
    for review in results:
            if review['content']: 
                collect_review(review, data, 0, app_id, app_title)
                
    return data

def download_some_reviews(app_id, data):
    this_app = app(app_id)
    app_title = this_app["title"]
    print("Downloading reviews for ", app_title)
    result, continuation_token = reviews(app_id, count=10000)
    for review in result:
        collect_review(review, data, 0, app_id, app_title)

    return data
    
def create_db(app_ids, fields):

    data = []
    for id in app_ids:
        data = download_some_reviews(id, data)
    
    df = pd.DataFrame(data, columns=fields)

    df = df.drop(columns="ID")
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": "ID"})

    df.to_csv("play_store_reviews.csv")


#Top 10 free apps according to google play store as of 7/18
top_free = ['com.zhiliaoapp.musically','com.babbel.mobile.android.en', 'com.squareup.cash', 
'com.instagram.android', 'com.engro.cleanerforsns', 'com.whatsapp',
'com.different.toonme', 'com.google.android.apps.dynamite', 'com.snapchat.android', 'com.mcdonalds.app']

test_sample = ['com.seattletimes.android.SeattleTimesMobileNews', 'com.nytimes.android', 'com.washingtonpost.android']

# create_db(top_free, FIELDS)
