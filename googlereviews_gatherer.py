from google_play_scraper import app, reviews_all, reviews
from gatherer.engine.melk_format import MelkRow
import datetime
import pandas as pd

# Note: this file is unfinished, untested, and is not integrated into the main gatherer flow. 
# search_reviews_db() gives functionality similar to the other gatherers, but it relies on having a local
# database of reviews in the data folder that we do not currently provide.
#  
# Use downloader/engine/google_reviews_downloader.py to create this database, then pass this location 
# along with keyword and dates to search_reviews_db(). This will return a dataframe with 
# only the rows from the database we collected that match the query. 

def search_reviews_db(keyword, start_date, end_date, db_file):
    # gets reviews from local/pre-collected database. 
    # Expects this to already be in Melk format, returns a dataframe with only rows that match query. 
    # Search is case sensitive and exact- keyword must match app title precisely.   
    # TODO- implement date filtering. 

    db = pd.read_csv(db_file)
    results = db[db['SECTION'] == keyword]
    
    return results 

