import tweepy

# http://docs.tweepy.org/en/latest/extended_tweets.html

TWITTER_API_KEY = "nMSlQpR04UHcw8w5PcMY96Xay"
TWITTER_API_SECRET = "cxCCXR0JWP98OafacNOX46AZsuCRfGqZs5MW3XF11VfLKmQZaD"

consumer_key = TWITTER_API_KEY
consumer_secret = TWITTER_API_SECRET

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
# for tweet in tweepy.Cursor(api.search, q="tweepy").items(10):
#     print(tweet.text)
user = api.get_user(screen_name="HyparAEC")
timeline = api.user_timeline(screen_name="HyparAEC")

# Only iterate through the first 200 statuses
# tweepy.Cursor(api.user_timeline, id="twitter")
# for status in tweepy.Cursor(api.user_timeline).items(200):
#     process_status(status)


# status = api.get_status(id, tweet_mode="extended")
# try:
#     print(status.retweeted_status.full_text)
# except AttributeError:  # Not a Retweet
#     print(status.full_text)
