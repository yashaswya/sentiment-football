import os
import tweepy as tw
import pandas as pd
import time
consumer_key = 'oY8d4FkbRwsKYr9aAWcwzVz9j'
consumer_secret = '8CBzW2HoPuYHcLJUrsmSbKUeb9tzBlJr5OiyYYZaO6YiKUGgNY'
access_token ='717871884-LXDjAhZPLvnme6wDFfPa6EDTDYRBqVBVKg1Ibyue'
access_token_secret = 'B0QOk12TObG8f25HqgLJmFmbef4U2NGuPULvk4HIJ2Ze6'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "#ManCity -filter:retweets"
date_since = "2020-07-15"

# Search for the tweets
print("Tweets downloading...")
start_time=time.time()
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since).items(300)

# Iterate over tweets to get selective data
users_tweets = [[tweet.user.screen_name, tweet.user.location, tweet.text, tweet.favorite_count] for tweet in tweets]

# Create a pandas DataFrame and converting into CSV
tweet_text = pd.DataFrame(data=users_tweets, columns=['user', "location", "tweet", "favorite"])
tweet_text.to_csv("api_data_ManCity_16thJuly.csv")
end = time.time()
print("{0} tweets have been downloaded in {1} secs.".format(len(tweet_text), end-start_time))