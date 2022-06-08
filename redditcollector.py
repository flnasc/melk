from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

FIELDS = ['ID', 'SOURCE', 'SECTION', 'SOURCE_URL', 'DATE', 'TITLE', 'FULL_TEXT', 'TYPE']
SOURCE_NAME = "reddit"
TYPE = "post"

def download_posts(keyword, start_date, end_date): 
    #start_date and end_date expected as strings in ISO format (YYYY-MM-DD)

    api = PushshiftAPI()

    start = int(dt.datetime.fromisoformat(start_date).timestamp())
    print("start = ", start)
    end = int(dt.datetime.fromisoformat(end_date).timestamp())
    print("end = ", end)

    #start2 = dt.datetime(2017, 1, 1).timestamp()
    #print("start2 = ", start2)

    #returns generator object with submissions 
    ####LIMIT=100 for testing#### 
    gen = api.search_submissions(limit=100, q='metaverse', 
                            filter=['url','title','subreddit','created_utc','selftext'], 
                            after=start, 
                            before=end)
    
    data=[]
    good_posts = 0
    bad_posts = 0
    next_id = 0
    
    for post in gen:  

        if (post.selftext and post.selftext != "[deleted]" and post.selftext != "[removed]"):
            #print("Post: ", post.d_, "\n")
            #print("***********Processing post**************")
            #print("Title: ", post.title)
            #print("Author: ", post.author)
            #print("URL: ", post.url)
            #print("subreddit: ", post.subreddit)
            #print("created_utc: ", post.created_utc)
            #print("selftext: ", post.selftext)
            good_posts += 1
            reddit_parser(post, data, next_id)
            next_id += 1
        else:
            #print("NO TEXT/REMOVED/DELETED")
            #print("URL: ", post.url)
            #print("selftext: ", post.selftext)
            bad_posts += 1

    print(good_posts, " of 100 are good posts.")

    df = pd.DataFrame(data, columns=FIELDS)

    return df 

def reddit_parser(post, data, next_id):
    
    #print("parsing post")
    this_post = {'ID': next_id,
                 'SOURCE': SOURCE_NAME, 
                 'SECTION': post.subreddit, 
                 'SOURCE_URL': post.url, 
                 'DATE': (dt.datetime.utcfromtimestamp(post.created_utc).date()), 
                 'TITLE': post.title, 
                 'FULL_TEXT': post.selftext, 
                 'TYPE': TYPE}
    #print(this_post)
    data.append(this_post)

    #df = df.append(this_post, ignore_index=True)
    #print(df)
    #return df

#def test():
    #df = download_posts('metaverse', '2017-01-01', '2022-06-08')
    #df.to_csv('./example_out.csv', index=False)

    #one = 1654660800
    #two = dt.datetime.utcfromtimestamp(one).date()
    #print(two)

    
 
#test()





#reddit = praw.Reddit(
#    client_id="pYMiw37j0X1YqwtuYscjLA",
#    client_secret="ajbospKnL4UXRRV6Il3nO26L2NTmlQ",
#    user_agent="mac:TestCollector:v0 (by u/ProjectMelk)"
#)

#print(reddit.read_only)

#for post in reddit.subreddit("ultralight").hot(limit=1):
#    print(post.title)
#    #pprint.pprint(vars(post))
#    top_level_comments = list(post.comments)
#    all_coments =post.comments.list()
#    for comment in top_level_comments:
#        pprint.pprint(vars(comment))