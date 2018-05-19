import tweepy
import json
import os
from time import sleep
import sys

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

with open(dir_path + '/../config.json', 'r') as f:
	config = json.load(f)

KEY = config['twitter']['key']
SECRET = config['twitter']['secret']

# set up the API key
auth = tweepy.AppAuthHandler(KEY, SECRET)
api = tweepy.API(auth)
max_items = 3200 # most we can get from a single user

# grab the tweets
# @param String screenname
# @returns List[{Tweets}]
def grab_tweets(sn):
	tweets = tweepy.Cursor(api.user_timeline, screen_name = sn).items(max_items)
	tweets = [t._json for t in tweets]
	return tweets

# write tweets to disk, out/{screenname}/tweets.json
# will overwrite whatever's in the file
# TODO: Inspect already downloaded tweets, 
# get max_id, only look for later ones and append
# @param String sn
def write_tweets(tweets, sn):
	directory = dir_path + '/../out/' + sn
	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(directory + '/tweets.json', 'w', encoding = 'utf8') as f:
		json.dump(tweets, f)


# read in users, let's actually grab the tweets
with open('./users.txt') as f:
	users = f.readlines()
	users = [u.strip() for u in users]

print('Found {} users data to grab'.format(len(users)))
print('Beginning to grab tweets for users, this may take a while...')

to_finish = len(users)
finished = 0

# Don't hammer the API, limit is 900 requests per 15 minute windows
# NB each call to cursor can be up to 3200 / 200 = 16 requests
for user in users:
	sleep(10)
	tweets = grab_tweets(user)
	write_tweets(tweets, user)
	finished += 1
	print('Finished fetching {}/{} user\'s tweets'.format(finished, to_finish))

print('Finished fetching all user\'s tweets')



