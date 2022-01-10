import tweepy
from pymongo import MongoClient
import keys

def extract_tweets():
    auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    api = tweepy.API(auth)
    #Getting tweets from a particular user
    gagan_tweets = api.home_timeline('gagandayal')
    tweet_list = []
    for tweet in gagan_tweets:
        id = tweet.id
        text = tweet.text
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        status = {'tweet_id': id,
                  'text': text,
                  'favorite_count': favorite_count,
                  'retweet_count': retweet_count,
                  }
        tweet_list.append(status)
    print(tweet_list)
    client = MongoClient("mongodb+srv://gagandayal:gagandeep123@gagandayal.otj9q.mongodb.net/twitter?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client["DataMiningAssignment2"]
    collection = db["twitterData"]
    collection.insert_many(tweet_list)

extract_tweets()