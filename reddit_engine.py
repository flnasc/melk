from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

FIELDS = ['ID', 'SOURCE', 'SECTION', 'SOURCE_URL', 'DATE', 'TITLE', 'FULL_TEXT', 'TYPE']
SOURCE_NAME = "reddit"
TYPE = "post"

def search_reddit(keyword, start_date, end_date):
    #takes dates as date objects. returns dataframe with collected posts in Melk format (see data). 

    api = PushshiftAPI()

    start = dt.datetime(start_date.year, start_date.month, start_date.day)
    start = int(start.timestamp())
    end = dt.datetime(end_date.year, end_date.month, end_date.day)
    end = int(end.timestamp())

    #####LIMIT = 100 FOR TESTING ONLY 
    gen=api.search_submissions(limit=100, q=keyword, 
                               filter=['url', 'title', 'subreddit', 'created_utc,', 'selftext'],
                               after=start, before=end)

    data = []
    posts_collected = 0
    next_id = 0

    for post in gen:
        if (post.selftext and post.selftext != "[deleted]" and post.selftext != "[removed]"):
            collect_post(post, data, next_id)
            posts_collected += 1
            next_id += 1
    
    df = pd.DataFrame(data, columns=FIELDS)
    print("Success! Collected ", posts_collected, " posts from Reddit.")

    return df

def collect_post(post, data, next_id):
    this_post = {'ID': next_id,
                 'SOURCE': SOURCE_NAME, 
                 'SECTION': post.subreddit, 
                 'SOURCE_URL': post.url, 
                 'DATE': (dt.datetime.utcfromtimestamp(post.created_utc)), 
                 'TITLE': post.title, 
                 'FULL_TEXT': post.selftext, 
                 'TYPE': TYPE}
    data.append(this_post)
