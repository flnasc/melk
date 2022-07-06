import datetime as dt
import pandas as pd
import json
import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Gets API keys from apiconfig.py file on your machine.
# This file must be created and filled in prior to use.
# See apiconfig_example.py.
import apiconfig


SOURCE_NAME = "new_york_times"
TYPE = "article"
ARTICLES_PER_PAGE = 10
# The Article Search API provides results in pages of 10 articles each.

# USER_LIMIT = 100
USER_LIMIT = float("inf")


def search_nyt(keyword, start_date, end_date, fields):
    # takes dates as date objects. searches with NYT Article Search API.
    # returns a pandas dataframe with collected articles in Melk format (see data dictionary).

    results_page = 0
    next_page = True
    data = []
    total_articles = 0

    while next_page is True:

        if total_articles >= USER_LIMIT:
            next_page = False
            break

        # loop through pages of API results

        articles_collected = download_one_page(
            keyword, start_date, end_date, results_page, data, total_articles
        )
        total_articles += articles_collected

        if articles_collected < ARTICLES_PER_PAGE:
            next_page = False

        results_page += 1

        # NYT API rate cap is 10 requests/minute
        time.sleep(6)

    df = pd.DataFrame(data, columns=fields)

    print("Success! Collected ", total_articles, " articles from The New York Times.")

    return df


def download_one_page(keyword, start_date, end_date, results_page, data, next_id):

    articles_collected = 0

    # build API call
    api_prefix = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    api_query = "q=" + keyword
    api_filter = (
        "&begin_date="
        + start_date.strftime("%Y")
        + start_date.strftime("%m")
        + start_date.strftime("%d")
        + "&end_date="
        + end_date.strftime("%Y")
        + end_date.strftime("%m")
        + end_date.strftime("%d")
    )
    api_page = "&page=" + str(results_page)
    api_key = "&api-key=" + apiconfig.new_york_times_api_key
    api_call = api_prefix + api_query + api_filter + api_page + api_key

    # retrieve JSON
    page_meta = requests.get(api_call)
    page_meta_list = json.loads(page_meta.text)

    print("Downloading page ", results_page, " of NYT results....")

    for doc in page_meta_list["response"]["docs"]:
        if doc["document_type"] == "article":
            parse_article(doc, data, next_id)
            articles_collected += 1
            next_id += 1

    return articles_collected


def parse_article(article, data, next_id):

    this_article = {
        "ID": next_id,
        "SOURCE": SOURCE_NAME,
        "SECTION": article["section_name"],
        "SOURCE_URL": article["web_url"],
        #'DATE': article['pub_date'],
        "DATE": dt.datetime.fromisoformat(article["pub_date"].split("+")[0]),
        "TITLE": article["headline"]["main"],
        #'FULL_TEXT': scrape_content(article['web_url']),
        "FULL_TEXT": scrape_body_text(article["web_url"]),
        "TYPE": TYPE,
    }

    data.append(this_article)

    return


def scrape_body_text(url):
    session = HTMLSession()
    page = session.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # NYT archive webpages use <p class="css-at9mc1 evys1bk0"> elements for article body
    ps = soup.find_all("p", class_="css-at9mc1")

    content = ""
    for p in ps:
        content = content + p.text + " "

    return content


def test():
    s = dt.date.fromisoformat("1900-01-01")
    e = dt.date.fromisoformat("2000-01-01")
    search_nyt(
        "bank",
        s,
        e,
        ["ID", "SOURCE", "SECTION", "SOURCE_URL", "DATE", "TITLE", "FULL_TEXT", "TYPE"],
    )


# test()
