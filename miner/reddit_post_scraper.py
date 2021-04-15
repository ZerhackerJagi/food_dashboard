import praw
from datetime import datetime
import mysql.connector

QUERY = "INSERT INTO reddit(hour_created, time_created, day_created, author, title, ups, downs, num_comments, text, thumbnail, url, curr_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
API_KEY_REDDIT = "XXX"
API_CLIENTID_REDDIT = "XXX"
USERNAME_REDDIT = "XXX"
PW_REDDIT = "XXX"
LIMIT_REDDIT_POSTS = 100


db = mysql.connector.connect(
  host="localhost",
  user="user",
  password="password",
  database="reddit"
)


reddit = praw.Reddit(client_id = API_CLIENTID_REDDIT,
                    client_secret = API_KEY_REDDIT,
                    username= USERNAME_REDDIT,
                    password = PW_REDDIT,
                    user_agent = "food_dashboard_v01")

sr = reddit.subreddit("food")

# retrieve new posts
new_posts = sr.hot(limit=LIMIT_REDDIT_POSTS)
mycursor = db.cursor()

# clean data
for post in new_posts:
  timestamp_created = post.created
  time_created = datetime.fromtimestamp(timestamp_created).strftime("%H:%M:%S")
  day_created = datetime.fromtimestamp(timestamp_created).strftime("%Y-%m-%d")
  hour_created = datetime.fromtimestamp(timestamp_created).strftime("%H")

  # insert data into db

  vals = (hour_created,
          time_created,
          day_created,
          post.author.name,
          post.title,
          post.ups,
          post.downs,
          post.num_comments,
          post.selftext,
          post.thumbnail,
          post.url,
          datetime.now())
  mycursor.execute(QUERY, vals)

db.commit()
