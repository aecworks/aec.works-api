import tweepy
from django.conf import settings


def get_tweepy_client():
    auth = tweepy.AppAuthHandler(
        settings.OAUTH_TWITTER_API_KEY, settings.OAUTH_TWITTER_API_SECRET
    )
    return tweepy.API(auth)


def get_timeline(handle, num=5):
    client = get_tweepy_client()
    items = []
    for item in tweepy.Cursor(client.user_timeline, screen_name=handle).items(num):
        items.append(item._json)
    return items
