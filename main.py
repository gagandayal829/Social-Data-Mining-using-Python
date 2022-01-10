from flask import Flask, request, render_template
from pymongo import MongoClient
import keys
import tweepy
import datetime as dt
import praw

app = Flask(__name__, template_folder='newTemplates')

# Creating mongodb connection
client= MongoClient("mongodb+srv://gagandayal:gagandeep123@gagandayal.otj9q.mongodb.net/twitter?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.DataMiningAssignment2

#Performing Reddit Authentication
redditAuth = praw.Reddit(client_id=keys.ClientID,
                         client_secret=keys.ClientSecretID,
                         username=keys.UserName,
                         password=keys.Password,
                         user_agent=keys.UserAgent)

# Performing Twitter Authentication
auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

@app.route('/')
def shows():
    return render_template("index.html")

@app.route('/redditForm')
def redditForm():
    return render_template("reddit.html")

@app.route('/twitterForm')
def twitterForm():
    return render_template("twitter.html")

@app.route('/redditUpdate', methods=['POST'])
def redditUpdate():
    title = request.values.get("title")
    status = request.values.get("status")
    sub = redditAuth.subreddit("Warzone")
    update = sub.submit(title,status)
    collection= db.redditData
    collection.insert_one({
        "postId": update.id,
        "postAuthor": update.author.name,
        "postTitle": update.title,
        "postText": update.selftext,
        "postDate":dt.datetime.fromtimestamp(update.created).strftime("%b %d %Y %H:%M:%S"),
        "postScore": update.score
    })

    return render_template('index.html')

@app.route('/twitterUpdate', methods=['POST'])
def twitterUpdate():
    tweet= request.values.get("status")
    update= api.update_status(tweet)
    collection = db.twitterData
    collection.insert_one({
        "tweetID": str(update.id),
        "tweetAuthor": update.author.name,
        "tweetText": update.text,
        "tweetDate": update.created_at.strftime("%b %d %Y %H:%M:%S"),
        "tweetLang": update.lang,
        "retweetCount": update.retweet_count,
        "tweetSource": update.source
    })
    return render_template('index.html')

if __name__ == '__main__':
    app.debug= True
    app.run()