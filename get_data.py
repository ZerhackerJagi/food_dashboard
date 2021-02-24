'''

Hier ist nur das Datengelade in einem extra File.
Wenn man das File ausführt, speichert man den Datenbankauszug in einer Excel.

'''


import praw
import pandas as pd
from datetime import datetime
import requests
import json
import mysql.connector
# excel file creation
import openpyxl


def get_data_as_df():

    # Final Variablen
    API_KEY_SPOONACULAR = "146fe79a630b4afb8306a2985bedc64c"
    API_KEY_REDDIT = "KAJ2xGzCOlH3hyTRADNdSBDuTBORvw"
    API_CLIENTID_REDDIT = "tSemvcUBRFCTYQ"

    USERNAME_REDDIT = "Short-Arrival7632"
    PW_REDDIT = "cookies123"

    # KONFIGURATION
    LIMIT_REDDIT_POSTS = 100
    LIMIT_SPOONACULAR_RECIPES = 5


    # DATA BANK 
    db_connection = mysql.connector.connect(
      host= "wp.jagi.wtf",
      user= "redditu",
      password= "redditMaster",
      database="reddit"
      )

    cursor = db_connection.cursor()

    cursor.execute("SELECT count(id) FROM reddit")
    res = cursor.fetchall()

    # GET SUBREDDIT DATA
    reddit = praw.Reddit(client_id = API_CLIENTID_REDDIT,
                        client_secret = API_KEY_REDDIT,
                        username= USERNAME_REDDIT,
                        password = PW_REDDIT,
                        user_agent = "food_dashboard_v01")

    sr = reddit.subreddit("food")

    # retrieve new posts
    new_posts = sr.hot(limit=LIMIT_REDDIT_POSTS)

    # clean data 
    new_posts_lst = []
    for post in new_posts:
        timestamp_created = post.created
        time_created = datetime.fromtimestamp(timestamp_created).strftime("%H:%M:%S")
        day_created = datetime.fromtimestamp(timestamp_created).strftime("%Y-%m-%d")
        hour_created = datetime.fromtimestamp(timestamp_created).strftime("%H")

        # created time, created day, author, title, likes, downs, num_comments, text, thumbnail, url
        x = [hour_created, time_created, day_created, post.author, post.title, post.ups, post.downs, post.num_comments, post.selftext, post.thumbnail, post.url]
        new_posts_lst.append(x)

    # create DataFrame
    df = pd.DataFrame(data=new_posts_lst, columns=["hour_created", "created_time", "created_day", "author", "title", "likes", "downs", "num_comments", "text", "thumbnail", "url"])

    return df

###################################################

if __name__ == "__main__":

    df = get_data_as_df()
    
    df.to_excel("data.xlsx")  