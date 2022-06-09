from nyt_engine import search_nyt
from reddit_engine import search_reddit
import pandas as pd 
import datetime as dt
import numpy as np

#driver(keyword, start_date, end_date, scope, sources)
    #expects keyword as single string
    #expects dates as strings in iso format [YYYY-MM-DD]
    #expects sources as list of strings
    #calls nyt_engine, reddit_engine, other engines
    #concatenates into one dataframe 
    #could clean data? 
    #could do some analysis? 
    #save df to csv file
    
def driver(keyword, start_date, end_date, scope, sources): 

    start_date = dt.date.fromisoformat(start_date)
    end_date = dt.date.fromisoformat(end_date)

    nyt = pd.DataFrame()
    reddit = pd.DataFrame()

    for source in sources:
        print(source)
        if (source == "new_york_times"):
            print("Searching New York Times Archive....")
            nyt = search_nyt(keyword, start_date, end_date)
            #print(nyt.DATE)
            #print(nyt)

        if (source == "reddit"):
            print("Searching Reddit....")
            reddit = search_reddit(keyword, start_date, end_date)
            #print(reddit.DATE)

        df = pd.concat([nyt, reddit], ignore_index=True)

        df.to_csv('./outputs/metaverse_test.csv')
    #df = nyt + reddit
    #filename_out = keyword_YYYY-MM-DD_YYYY-MM-DD.csv
    #df.to_csv(filename_out)
   
def test():
    driver('metaverse', '2022-06-01', '2022-06-08', 'doc', ["new_york_times","reddit"])

test()       
