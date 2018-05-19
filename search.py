import tweepy

from config import CONSUMER_KEY
from config import CONSUMER_SECRET

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

arg = { 'username' : 'albatrossninja' }
tweets = api.user_timeline(screen_name = 'x')