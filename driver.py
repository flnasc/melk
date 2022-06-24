from operator import index
from nyt_engine import search_nyt
from reddit_engine import search_reddit
import pandas as pd 
import datetime as dt

#Defining Melk format - see data dictionary for more info 
FIELDS = ['ID', 'SOURCE', 'SECTION', 'SOURCE_URL', 'DATE', 'TITLE', 'FULL_TEXT', 'TYPE']

#driver(keyword, start_date, end_date, scope, sources)
    #expects keyword as single string
    #expects dates as strings in iso format [YYYY-MM-DD]
    #expects sources as list of strings in any order
    #calls nyt_engine, reddit_engine, other engines
    #concats into one dataframe 
    #then, could clean data
    #could do some analysis 
    #save df to csv file
    
def driver(keyword, start_date, end_date, scope, sources): 

    start_date = dt.date.fromisoformat(start_date)
    end_date = dt.date.fromisoformat(end_date)

    nyt = pd.DataFrame()
    reddit = pd.DataFrame()

    for source in sources:
        if (source == "new_york_times"):
            print("Searching New York Times Archive....")
            nyt = search_nyt(keyword, start_date, end_date, FIELDS)

        if (source == "reddit"):
            print("Searching Reddit....")
            reddit = search_reddit(keyword, start_date, end_date, FIELDS)

    df = pd.concat([nyt, reddit], ignore_index=True)
    #replace ID column with updated column that accounts for rows from other sources
    df = df.drop(columns='ID')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index':'ID'})

    filename_out = './outputs/' + keyword + '_' + start_date.isoformat() + '_' + end_date.isoformat() + '.csv'
    df.to_csv(filename_out)    

