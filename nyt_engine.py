import datetime as dt
import pandas as pd
import json
import pprint
import time
import requests
from requests_html import HTMLSession

FIELDS = ['ID', 'SOURCE', 'SECTION', 'SOURCE_URL', 'DATE', 'TITLE', 'FULL_TEXT', 'TYPE']
SOURCE_NAME = "new_york_times"
TYPE = "article"

ARTICLES_PER_PAGE = 10
#Article search API provides results in pages of 10 articles each.
 




# ******* CONTAINS PRIVATE API KEY DO NOT PUBLISH **********




def search_nyt(keyword, start_date, end_date):
    #takes dates as date objects. searches with NYT archive API. 
    #returns a pandas dataframe with collected articles in Melk format (see data dictionary).

    results_page = 0
    next_page = True
    data = []
    total_articles = 0

    while next_page is True:
    #loop through pages of API results

        articles_collected = download_one_page(keyword, start_date, end_date, results_page, data, total_articles)
        total_articles += articles_collected

        if (articles_collected < ARTICLES_PER_PAGE):
            next_page = False

        results_page += 1

        #NYT API rate cap is 10 requests/minute
        time.sleep(6)

    df = pd.DataFrame(data, columns=FIELDS)

    print("Success! Collected ", total_articles, " articles from The New York Times.")

    return df

def download_one_page(keyword, start_date, end_date, results_page, data, next_id):

    articles_collected = 0

    #build API call 
    api_prefix = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_query = 'q=' + keyword
    api_filter = "&begin_date="+start_date.strftime("%Y")+start_date.strftime("%m")+start_date.strftime("%d")+"&end_date="+end_date.strftime("%Y")+end_date.strftime("%m")+end_date.strftime("%d")
    api_page = '&page=' + str(results_page)
    api_key = '&api-key=64d0YdzbSTBTBkBKtAJ2J2bMfbn57T8X'
    api_call = api_prefix + api_query + api_filter + api_page + api_key

    #retrieve JSON 
    page_meta = requests.get(api_call)
    page_meta_list = json.loads(page_meta.text)

    for doc in page_meta_list['response']['docs']:
        parse_article(doc, data, next_id)
        articles_collected += 1
        next_id += 1

    return articles_collected

def parse_article(article, data, next_id):

    this_article = {'ID': next_id,
                 'SOURCE': SOURCE_NAME, 
                 'SECTION': article['section_name'], 
                 'SOURCE_URL': article['web_url'], 
                 'DATE': article['pub_date'],
                 'TITLE': article['headline']['main'], 
                 'FULL_TEXT': scrape_content(article['web_url']), 
                 'TYPE': TYPE}

    data.append(this_article)
    
    return

def scrape_content(web_url):

    session = HTMLSession()
    page = session.get(web_url)

    #NYT archive webpages use <p class="css-at9mc1 evys1bk0"> elements for article body
    paragraphs = page.html.find("p.css-at9mc1")

    #paragraphs.append(page.html.find("p.css-8hvvyd"))
    content = ""
    for i in range(len(paragraphs)):
        content = content + paragraphs[i].text + " "

    return content
  

def test():
    f = open('example.json')

    data = json.load(f)

    #pprint.pprint(data)

    print(data['response']['docs'][0])

    for doc in data['response']['docs']:
        print(doc['headline']['main'])
    

#test()
