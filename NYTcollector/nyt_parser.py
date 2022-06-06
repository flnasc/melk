from asyncore import write
import csv 
import xml.etree.ElementTree as ET
#import pandas as pd 

SOURCE_NAME = "new_york_times"
TYPE = "article"
FIELDS = ['ID', 'SOURCE', 'SECTION', 'SOURCE_URL', 'DATE', 'TITLE', 'FULL_TEXT', 'TYPE']

#parse_xml converts an XML file (from nyt_downloader) into a CSV file that maps 
#data into the standard fields defined by the data dictionary
#xmlfile: the file to be read from and parsed
#csvfile: the file to write out to 
#current_id: the current object ID number for ProjectMelk collection. If old file ends with an item that has id "55", use "56" as current_id
#   0 for testing, but if ProjectMelk has collected from other sources or files already, could be higher
#usage: nyt_parser xmlfile csvfile current_id

def parse_xml(xmlfile, csvfile, current_id):

    tree = ET.parse(xmlfile)
    root = tree.getroot()
    dicts = []
    current_id = int(current_id)

    for article in root.findall('./article'): 
        
        this_article = {'ID': '', 'SOURCE': '', 'SECTION': '', 'SOURCE_URL': '', 'DATE': '', 'TITLE': '', 'FULL_TEXT': '', 'TYPE': ''}
        this_article['ID'] = current_id
        current_id += 1
        this_article['SOURCE'] = SOURCE_NAME
        this_article['TYPE'] = TYPE

        for child in article: 
            if child.tag == 'section':
                this_article['SECTION'] = child.text
            if child.tag == 'pub_date':
                this_article['DATE'] = child.text
            if child.tag == 'headline':
                this_article['TITLE'] = child.text
            if child.tag == 'content':
                this_article['FULL_TEXT'] = child.text
            if child.tag == 'web_url':
                this_article['SOURCE_URL'] = child.text

        dicts.append(this_article)

    with open(csvfile, 'w') as file:
        writer = csv.DictWriter(file, fieldnames = FIELDS)
        writer.writeheader()
        writer.writerows(dicts)

    return


# def parse_xml_pandas(xmlfile, current_id):
#   tree = ET.parse(xmlfile)
#    root = tree.getroot()
#    dicts = []
#    current_id = int(current_id)

#    for article in root.findall('./article'): 
        
#        this_article = {'ID': '', 'SOURCE': '', 'SECTION': '', 'SOURCE_URL': '', 'DATE': '', 'TITLE': '', 'FULL_TEXT': '', 'TYPE': ''}
#        this_article['ID'] = current_id
#        current_id += 1
#        this_article['SOURCE'] = SOURCE_NAME
#        this_article['TYPE'] = TYPE

#        for child in article: 
#            if child.tag == 'section':
#               this_article['SECTION'] = child.text
#            if child.tag == 'pub_date':
#                this_article['DATE'] = child.text
#            if child.tag == 'headline':
#                this_article['TITLE'] = child.text
#            if child.tag == 'content':
#                this_article['FULL_TEXT'] = child.text
#            if child.tag == 'web_url':
#                this_article['SOURCE_URL'] = child.text

#        dicts.append(this_article)
    
 
#    df = pd.DataFrame(dicts)

    #print(df)
    #print(df.loc[0, 'FULL_TEXT'])
#    for x in df.index:
#        if df.loc[x, "SOURCE_URL"] == "https://www.nytimes.com/2021/09/09/technology/facebook-wayfarer-stories-smart-glasses.html":
#            print(df.loc[x, "ID"])
#            print(df.loc[x, "SECTION"])

#    return


#if len(sys.argv) == 4:
#    print("xml: ", sys.argv[1], " csv: ", sys.argv[2], " id: ", sys.argv[3])
#    parse_xml(sys.argv[1], sys.argv[2], sys.argv[3])
    
#else: 
#    parse_xml('./articles/2000_12.xml', './articles/2000_12.csv', 0)

#parse_xml_pandas('./articles/nyt_articles_metaverse_2021-06-02_2022-06-02.xml', 0)
