from gatherer.engine import gatherer, nyt_gatherer, reddit_gatherer, twitter_gatherer, melk_format
import datetime as dt
import sys

"""
This file is intended to serve as a command line interface for the gatherer functionality. 
Primarily for demonstration purposes at the moment. 

Usage: In terminal, from project folder run "python3 melk.py"
    If  you have not already installed the required dependencies, 
    first run "pip install -r requirements.txt". 
    """

if __name__ == '__main__':

    print("Starting example search for 'Seattle' in the New York Times archive between 2015-01-01 and 2015-02-01....")
    print("View progress and current status in the log file by opening melk.log")
    
    filename_out = gatherer.gatherer("Seattle", "2015-01-01", "2015-02-01", "doc", ['new_york_times'])

    print("Search completed. Results are stored in the file", filename_out)
