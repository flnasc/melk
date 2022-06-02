import requests
import json
from   lxml import html
import xml.etree.cElementTree as ET
import logging
import sys
from requests_html import HTMLSession



logging.basicConfig(filename='./nyt_log.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

### Initial definitions

start_year  = int(sys.argv[1])
end_year    = int(sys.argv[2])

print("start year: ", start_year)
print("end year: ", end_year)

if len(sys.argv) == 4:
    start_month = int(sys.argv[3])
else:
    start_month = 1

end_month   = 13


api_prefix = 'https://api.nytimes.com/svc/archive/v1/'

#ProjectMelk key: 
api_suffix = '.json?api-key=64d0YdzbSTBTBkBKtAJ2J2bMfbn57T8X' 
api_sep = '/'

dest_dir = './articles/'
file_prefix = 'nyt_articles_'
file_extension = ".xml"

# Prepare XML structure
#root    = ET.Element("root")
#doc     = ET.SubElement(root, "doc")

doc     = ET.Element("doc")

for cur_year in range(start_year, end_year+1):

    for cur_month in range(start_month,end_month):

        logging.info("Working on month: " + str(cur_month) + " of year: " + str(cur_year))

        articles_meta = []

        ### Building request string
        request_string = api_prefix + str(cur_year) + api_sep + str(cur_month) + api_suffix
        print("request string: ", request_string)

        ### retrieving Jason
        one_month_meta_json = requests.get(request_string)

        print(one_month_meta_json)

        ## Parsing Jason into a list
        one_month_meta_list = json.loads(one_month_meta_json.text)

        ## Open Output Fil
        #meta_file_out = open(dest_dir + file_prefix + str(year) + '_' + str(cur_month) + file_extension, "w", encoding="utf8")
        filename_out = dest_dir + str(cur_year) + '_' + str(cur_month) + file_extension

        #file_out.write()

        hits = one_month_meta_list['response']['meta']['hits']

        #limit to ten articles download for testing  
        for i in range(hits):
        #for i in range(100):s

            logging.info("Writing Article: (" + str(cur_month) + "/"+ str(cur_year) + ") - "+ str(i) + " of " + str(hits))

            #print(one_month_meta_list['response']['docs'][i])

            try:
              web_url = (one_month_meta_list['response']['docs'][i]['web_url'])
              print("Article ", i, " web url: ", web_url)
            except IndexError:
              web_url = None

            try:
              pub_date = (one_month_meta_list['response']['docs'][i]['pub_date'].encode("utf8"))
              print("Article ", i, " pub_date: ", pub_date)
            except IndexError:
              pub_date = b" "

            try:
                if (('section_name' in one_month_meta_list['response']['docs'][i]) and (one_month_meta_list['response']['docs'][i]['section_name'] != None )):

                    section = (one_month_meta_list['response']['docs'][i]['section_name'].encode("utf8"))
                    print("Article ", i, " section: ", section)
                else:
                    section = b" "
            except IndexError:
                section = b" "

            try:
                if (one_month_meta_list['response']['docs'][i]['headline'] != []):
                    try:
                        headline = (one_month_meta_list['response']['docs'][i]['headline']['main'].encode("utf8"))
                        print("Article ", i, " headline: ", headline)
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


            ET.SubElement(article, "pub_date").text = pub_date.decode("utf-8")
            ET.SubElement(article, "web_url").text = web_url
            ET.SubElement(article, "section").text = section.decode("utf-8")
            ET.SubElement(article, "headline").text = headline.decode("utf-8")


            if (web_url != None):
              
                try:
                    ##Retrieve the page using https get method
                    #page = requests.get(web_url)

                    ##New method uses requests_html module, which handles new JavaScript on NYT website better: 
                    session = HTMLSession()
                    page = session.get(web_url)

                    paragraphs = page.html.find("p.css-at9mc1")
                    content = ""
                    for i in range(len(paragraphs)):
                        content = content + paragraphs[i].text + " "

                    ## creates a tree structure
                    #tree = html.fromstring(page.content)

                    ## Parse content out using the three common classes used by NYT html formatting standards
                    #content = tree.xpath('//div[@class="articleBody"]/text()')
                    #content = content + tree.xpath('//p[@class="story-body-text story-content"]/text()')
                    #content = content + tree.xpath('//p[@class="story-body-text"]/text()')
                    #content = content + tree.xpath('//p[@class="css-at9mc1 evys1bk0">]/text()')
                    #print(content)

                except:
                    content = " "
            else:
                content = " "

            ## Combine the list into a single string
            content_text = ''.join(content)

            print("Content text: ", content_text)

            content_text = content_text.encode("utf-8")

            #ET.SubElement(article, "content").text = "PLACEHOLDER FOR CONTENT"
            ET.SubElement(article, "content").text = content_text.decode("utf-8")


            #content_file_out.write(headline + '\n')
            #content_file_out.write(''.join(article))
            #content_file_out.write('\n' + '\n')

        ## Closing Output File
        # meta_file_out.close()
        # content_file_out.close()
        tree = ET.ElementTree(doc)
        tree.write(filename_out, encoding='utf-8', xml_declaration=True)
        #root.remove(doc)
        #doc = ET.SubElement(root, "doc")





