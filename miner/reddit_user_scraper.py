import praw
import pandas as pd
import time
from tqdm import tqdm
import mysql.connector

API_KEY_REDDIT = "XXX"
API_CLIENTID_REDDIT = "XXX"

USERNAME_REDDIT = "XXX"
PW_REDDIT = "XXX"


reddit = praw.Reddit(client_id = API_CLIENTID_REDDIT,
                    client_secret = API_KEY_REDDIT,
                    username= USERNAME_REDDIT,
                    password = PW_REDDIT,
                    user_agent = "food_dashboard_v01")

db_connection = mysql.connector.connect(
  host= "localhost",
  user= "user",
  password= "password",
  database="reddit"
  )

cursor = db_connection.cursor()


dfr = pd.read_sql("SELECT author FROM reddit GROUP BY author", db_connection)
df_author = dfr.to_dict()["author"]
author_count = len(df_author)

def get_insert_query_for_userdata_from_username(username, cursor, reddit, db_connection):
    QUERY = "INSERT INTO users(username, created_utc, is_mod, is_employee, link_karma) values (%s,%s,%s,%s,%s);"
    try:
        user = reddit.redditor(username)
        account_created = user.created_utc
        is_mod = user.is_mod
        is_employee = user.is_employee
        link_karma = user.link_karma
    except:
        account_created = 0
        is_mod=0
        is_employee=0
        link_karma=-1
    if not(account_created is None):
        vals = (username,
               account_created,
               int(is_mod),
               int(is_employee),
               link_karma)
        cursor.execute(QUERY, vals)
        time.sleep(1)
        print("next reddit user")
        db_connection.commit()
        return True
    time.sleep(20)
    return False
    

for i in tqdm(range(author_count)):
    get_insert_query_for_userdata_from_username(df_author[i], cursor, reddit, db_connection)

cursor.close()
db_connection.close()
