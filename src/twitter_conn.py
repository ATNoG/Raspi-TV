import twitter
import sqlite3 as sql
import os
from settings import *

conn = sql.connect(os.path.join(BASE_DIR, 'db/raspi-tv.sqlite'), check_same_thread=False)

(consumer_key, consumer_secret, access_token_key, access_token_secret) = conn.execute(
    'SELECT ConsumerKey, ConsumerSecret, AccessKey, AccessSecret FROM Twitter').fetchone()

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


def populate_db(query='%23raspi-tv', count=100):  # Containing '#raspi-tv'
    try:
        tweets = api.GetSearch(term=query, count=count)
        for tweet in tweets:
            conn.execute('INSERT OR REPLACE INTO Tweets (TweetId, Author, Tweet, ToDisplay) VALUES '
                         '(?, ?, ?, COALESCE((SELECT ToDisplay FROM Tweets WHERE TweetId=?), 0))',
                         (tweet.id, tweet.user.name, tweet.text, tweet.id))
            conn.commit()
    except twitter.TwitterError, e:
        print e
