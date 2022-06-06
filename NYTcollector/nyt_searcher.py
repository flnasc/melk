from datetime import datetime
import sys
import time
import xml.etree.cElementTree as ET
import requests
import json
from requests_html import HTMLSession
import time 
import argparse


from nyt_parser import parse_xml

ARTICLES_PER_PAGE = 10

#nyt_searcher takes as input a keyword query, a start date, and an end date. 
#Returns a .csv file with data from articles discovered through the NYT Article Search API

def download_articles(keyword, start_date, end_date):
    #creates xml file(s?)

    s = start_date
    e = end_date

    #destination directory
    dest_dir = './articles/'
    file_prefix = 'nyt_articles_'
    file_extension = '.xml'

    #create doc? 
    doc = ET.Element("doc")

    #open output file (just one output file per search for this program, unlike NYT_downloader)
    #includes dates in case we want to do searches for same term with different dates
    filename_out = dest_dir + file_prefix + keyword + '_' + start_date.isoformat() + '_' + end_date.isoformat() + file_extension
    
    #get each page of results from ArticleSearch
    results_page = 0
    next_page = True
    while next_page is True:

        hits = download_one_page(keyword, start_date, end_date, results_page, doc)
        #NYT API rate cap is 10 requests/minute
        time.sleep(6)
        #10 results per page
        if (results_page*ARTICLES_PER_PAGE) > hits:
            next_page = False
        else: 
            results_page += 1

    tree = ET.ElementTree(doc)
    tree.write(filename_out, encoding='utf-8', xml_declaration=True)
    print("writing to xml.....")
    csvfile = dest_dir + file_prefix + keyword + '_' + start_date.isoformat() + '_' + end_date.isoformat() + '.csv'
    print("parsing to csv.....")
    parse_xml(filename_out, csvfile, 0)
    print("done! results are store in " + csvfile)
    

    return

def download_one_page(keyword, start_date, end_date, results_page, doc):
    #build API call 
    api_prefix = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_query = 'q=' + keyword
    api_filter = "&begin_date=" + start_date.strftime("%Y") + start_date.strftime("%m") + start_date.strftime("%d") + "&end_date=" + end_date.strftime("%Y") + end_date.strftime("%m") + end_date.strftime("%d")
    api_page = '&page=' + str(results_page)
    api_key = '&api-key=64d0YdzbSTBTBkBKtAJ2J2bMfbn57T8X'
    api_call = api_prefix + api_query + api_filter + api_page + api_key

    #retrieve JSON 
    page_meta = requests.get(api_call)
    print(api_call)
    #parse into list
    page_meta_list = json.loads(page_meta.text)
        
    #add each article to xml tree
    #note: this crashes on the last page 
    #for i in range(ARTICLES_PER_PAGE):
    #note: below crashes after article 99
    #for i in range(len(page_meta_list['response']['docs'])):
    i = 0; 
    for item in page_meta_list['response']['docs']:   
        try: 
            web_url = item['web_url']
            #web_url = (page_meta_list['response']['docs'][i]['web_url'])
            print("Article ", (i+10*results_page), " web url: ", web_url)
        except IndexError:
            web_url = None
        
        try:
            pub_date = item['pub_date'].encode("utf8")
            # pub_date = (page_meta_list['response']['docs'][i]['pub_date'].encode("utf8"))
            #print("Article ", i, "pub date: ", pub_date)
        except IndexError:
            #why are we using byte literal? 
            pub_date = b" "

        try: 
            if ('section_name' in item['section_name'] and item['section_name'] != None):
                section = item['section_name'].encode("utf8")
            #if (('section_name' in page_meta_list['response']['docs'][i]) and (page_meta_list['response']['docs'][i]['section_name']!= None)):
                #section = (page_meta_list['response']['docs'][i]['section_name'].encode("utf8"))
                #print("Article ", i, " section: ", section)
            else: 
                section = b" "
        except IndexError:
            section = b" "

        try: 
            if item['headline'] != []:
                try: 
                    headline = item['headline']['main'].encode("utf8")
            #if (page_meta_list['response']['docs'][i]['headline'] != []):
                #try: 
                    #headline = (page_meta_list['response']['docs'][i]['headline']['main'].encode("utf8"))
                    print("Article ", (i+10*results_page), " headline: ", headline)
                except KeyError as e: 
                    headline = b" "
            else: 
                headline = b" "
        except IndexError: 
            headline = b" "
        
        article = ET.SubElement(doc, "article")

        if section == None:
            section = b''
        if article == None: 
            article = b''
        if pub_date == None:
            pub_date = b''
        if web_url == None: 
            web_url = b''
        
        ET.SubElement(article, "pub_date").text = pub_date.decode("utf8")
        #why did we encode everything except the web_url? 
        ET.SubElement(article, "web_url").text = web_url
        ET.SubElement(article, "section").text = section.decode("utf8")
        ET.SubElement(article, "headline").text = headline.decode("utf8")

        if (web_url != None): 
            try: 
                content = scrape_content(web_url)
            except: 
                content = b" "
        else: 
            content = b" "

        ET.SubElement(article, "content").text = content.decode("utf8")
        #print("Article ", i, " content: ", content.decode("utf8"))
        i += 1
    hits = page_meta_list['response']['meta']['hits']
    return hits

def scrape_content(web_url):
    session = HTMLSession()
    page = session.get(web_url)

    paragraphs = page.html.find("p.css-at9mc1")
    #paragraphs.append(page.html.find("p.css-8hvvyd"))
    content = ""
    for i in range(len(paragraphs)):
        content = content + paragraphs[i].text + " "

    content = content.encode("utf8")
    return content

def man_parse_command():
    if (len(sys.argv) != 4):
        print_usage()
        return
    else: 
        keyword = sys.argv[1]
        start_date = datetime.fromisoformat(sys.argv[2]).date()
        end_date = datetime.fromisoformat(sys.argv[3]).date()
        print("call: ", sys.argv[1], " ", sys.argv[2], " ", sys.argv[3])
        download_articles(keyword, start_date, end_date)

def print_usage():
    print("Error. Usage: nyt_searcher.py [keyword] [startdate] [enddate]")
    print("Example usage: nyt_searcher.py metaverse 2021-06-01 2022-06-02")




def test():
    start_date = datetime.date(2021, 6, 1)
    print("start date:  ", start_date)
    end_date = datetime.date(2022, 6, 1)
    print("end date: ", end_date)

    download_articles("metaverse", start_date, end_date)
    #doc = ET.Element("doc")
    #download_one_page("metaverse", start_date, end_date, 21, doc)
    #tree = ET.ElementTree(doc)
    #tree.write("./articles/test.xml", encoding='utf-8', xml_declaration=True)
    #parse_xml("./articles/test.xml", "./articles/test.csv", 210)


man_parse_command()
