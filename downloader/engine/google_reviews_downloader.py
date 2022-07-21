
# Note: this file is unfinished, untested, and is not integrated into the main gatherer flow. 
#  
# Rough documentation for creating a local database of reviews from specific apps of interest: 

# collect a list of app ids from google play store URLs for each app that you want to include reviews from in the database
# ex: the app id for spotify is 'com.spotify.music', which we find in the URL: https://play.google.com/store/apps/details?id=com.spotify.music

# With this list of app IDs ['com.spotify.music', 'com.nytimes.android', etc.], call create_db(list, fields). 
# Fields should be passed in from where it is defined in gatherer/engine/melkformat.py unless you are specifically
# trying to create a database with different columns. 
# Once this finishes collecting data (it may take a long time for apps with many reviews), 
# it should save as a csv file play_store_reviews.csv

from google_play_scraper import app, reviews_all, reviews
from gatherer.engine.melk_format import MelkRow
import datetime
import pandas as pd

SOURCE = "google_play_store"
TYPE = "app_review"

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
