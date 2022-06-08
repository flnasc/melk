#from nyt_engine import *
#from reddit_engine import *
from tracemalloc import start
import pandas as pd 
import datetime as dt


# nyt_engine 
#   main(keyword, start_date, end_date). takes dates as date objects. returns dataframe. 
# reddit_engine
#   main(keyword, start_date, end_date). takes dates as date objects. returns dataframe. 

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

    for source in sources:
        if (source == "new_york_times"):
            print("Searching New York Times Archive....")
            nyt = search_nyt(keyword, start_date, end_date)

        if (source == "reddit"):
            print("Searching Reddit....")
            reddit = search_reddit(keyword, start_date, end_date)

    #df = nyt + reddit
    #filename_out = keyword_YYYY-MM-DD_YYYY-MM-DD.csv
    #df.to_csv(filename_out)
    

def test():
    sources = ['new_york_times', 'reddit']
    driver('metaverse', '2022-06-07', '2022-06-08', 'doc', sources)

#test()       

