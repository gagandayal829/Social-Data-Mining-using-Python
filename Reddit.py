import praw
import datetime as dt
import keys
from pymongo import MongoClient

redditAuth = praw.Reddit(client_id=keys.ClientID,
                         client_secret= keys.ClientSecretID,
                         user_agent= keys.UserAgent,
                         user_name= keys.UserName,
                         password= keys.Password)

redditData = []

#for post in redditAuth.subreddit("Warzone").hot(limit=20):
for post in redditAuth.redditor("gagandayal").submissions.new():
    redditPosts ={
        "postId": post.id,
        "postAuthor": post.author.name,
        "postTitle": post.title,
        "postText": post.selftext,
        "postDate": dt.datetime.fromtimestamp(post.created).strftime("%b %d %Y %H:%M:%S"),
        "postScore": post.score
    }
    redditData.append(redditPosts)
client = MongoClient("mongodb+srv://*****:*****@****.otj9q.mongodb.net/twitter?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["DataMiningAssignment2"]
collection = db["redditData"]
collection.drop()
collection.insert_many(redditData)

print(redditData)
