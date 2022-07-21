# EXAMPLE configuration file.
# Before running the program, you need to get your own API keys
#   for each source that requires one, then add it to this file.
# Finally, make sure to save this file as "apiconfig.py" when finished.

new_york_times_api_key = None # "YOUR_API_KEY_HERE"
# See https://developer.nytimes.com/get-started

twitter_api_key = None # "YOUR_API_KEY_HERE"
search_tweets_bearer_token = None # "YOUR_API_KEY_HERE"
search_tweets_v2_endpoint = "https://api.twitter.com/2/tweets/search/all"

reddit_user_limit = float('inf')
nyt_user_limit = float('inf')

# Reminder: this comes out of the 10 million Tweet monthly cap per Academic API account
twitter_user_limit = float('inf') 

log_file = './melk.log'
poetry_dataset_path = "./data/poetry_foundation/poetry_foundation_full.csv"
sotu_dataset_path = "./data/state_of_the_union_data/"
billboard_dataset_path = "./data/billboard_songs/"
