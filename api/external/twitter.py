import tweepy
from django.conf import settings

# http://docs.tweepy.org/en/latest/extended_tweets.html

consumer_key = settings.TWITTER_API_KEY
consumer_secret = settings.TWITTER_API_SECRET

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


def get_timeline(twitter_handle):
    items = []
    for item in tweepy.Cursor(api.user_timeline, screen_name=twitter_handle).items(10):
        item.id
        item.text  # text
        item.created_at
        item.entities["hashtags"]
        items.append(item._json)
    return items


get_timeline("gtalarico")
# user = api.get_user(screen_name="HyparAEC")
# timeline = api.user_timeline(screen_name="HyparAEC")
# breakpoint()
# Only iterate through the first 200 statuses
# tweepy.Cursor(api.user_timeline, id="twitter")
# for status in tweepy.Cursor(api.user_timeline).items(200):
#     process_status(status)
# tweepy.Cursor(api.user_timeline, id="twitter")
# for status in tweepy.Cursor(api.user_timeline).items(200):
#     process_status(status)


# status = api.get_status(id, tweet_mode="extended")
# try:
#     print(status.retweeted_status.full_text)
# except AttributeError:  # Not a Retweet
#     print(status.full_text)
