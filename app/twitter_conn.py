import twitter
from constants import conn

(consumer_key, consumer_secret, access_token_key, access_token_secret) = conn.execute(
        'SELECT ConsumerKey, ConsumerSecret, AccessKey, AccessSecret FROM Twitter').fetchone()

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


def populate_db(query='@detiuaveiro', count=100):
    try:
        tweets = api.GetSearch(term=query, count=count)
        for tweet in tweets:
            conn.execute('INSERT OR REPLACE INTO Tweets (TweetId, Author, Tweet, ToDisplay) VALUES '
                         '(?, ?, ?, COALESCE((SELECT ToDisplay FROM Tweets WHERE TweetId=?), 0))',
                         (tweet.id, tweet.user.name, tweet.text, tweet.id))
            conn.commit()
    except twitter.TwitterError, e:
        print e
