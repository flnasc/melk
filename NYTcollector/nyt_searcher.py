import datetime
from time import strftime



#nyt_searcher takes as input a keyword query, a start date, and an end date. 
#Returns a .csv file with data from articles discovered through the NYT Article Search API

def download_articles(keyword, start_date, end_date):
    #creates xml files


    s = start_date
    e = end_date
 
    api_prefix = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_query = 'q=' + keyword
    api_filter = "&begin_date=" + s.strftime("%Y") + s.strftime("%m") + s.strftime("%d") + "&end_date=" + e.strftime("%Y") + e.strftime("%m") + e.strftime("%d")
    api_key = '&api-key=64d0YdzbSTBTBkBKtAJ2J2bMfbn57T8X'

    api_call = api_prefix + api_query + api_filter + api_key
    print(api_call)


    return

def parse_xml_to_csv(xmlfile, csvfile, startingrow_id):
    #accepts an xml file and parses it into a csv file
    #question: accept multiple files and put them into one? add on to the end of an existing file if it already has
    return


def driver(keyword, start_date, end_date):
    download_articles(keyword, start_date, end_date)
    
    #for each year in date range
        #for each month in date range
            #parse_xml_to_csv(xmlfile, csvfile, startingrow_id)


def test():
    start_date = datetime.date(2021, 6, 1)
    print("start date:  ", start_date)
    end_date = datetime.date(2022, 6, 1)
    print("end date: ", end_date)

    download_articles("metaverse", start_date, end_date)

test()