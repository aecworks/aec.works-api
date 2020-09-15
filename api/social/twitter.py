import tweepy
from django.conf import settings

consumer_key = settings.TWITTER_API_KEY
consumer_secret = settings.TWITTER_API_SECRET

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


def get_timeline(twitter_handle, num=5):
    items = []
    for item in tweepy.Cursor(api.user_timeline, screen_name=twitter_handle).items(num):
        items.append(item._json)
    return items
