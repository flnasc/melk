import requests
from requests_html import HTMLSession

#example for downloading text from NYT article page

SOURCE = "https://www.nytimes.com/2000/12/01/sports/pro-basketball-nets-slide-is-an-early-test-for-scott.html"

session = HTMLSession()

page = session.get(SOURCE)

#As of May 2022, NYT stores body text in <p class="css-at9mc1 evys1bk0"></p>
paragraphs = page.html.find("p.css-at9mc1")
text = ""
for i in range(len(paragraphs)):
    
    text = text + paragraphs[i].text + " "

print(text)



