import tweepy
import json
import os
import re
import glob

# load all the words we want to match with, compile regexes
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
with open(dir_path + '/../words.txt', 'r') as f:
	words = f.readlines()
	words = [w.strip() for w in words]

regs = map(lambda w: re.compile(w, re.I | re.U), words)
regs = list(regs)


# see if the text of a tweet object matches a pattern 
# @param tweet Twitter dict object
# @param regex pre-compiled regex object
def match(tweet, regex):
	m = regex.search(tweet['text'])
	print(m)
	if m:
		return True
	return False

def build_url(id):
	return "https://twitter.com/statuses/" + str(id)

# write searched to disk
def write_matches(matches, sn):
	directory = dir_path + '/../out/' + sn
	with open(directory + '/matches.json', 'w', encoding = 'utf8') as f:
		json.dump(matches, f)

# we need to go through every user's tweets, load one at a time
out_path = dir_path + '/../out/'
dirs = os.listdir(out_path)

to_finish = len(dirs)
finished = 0

print('Found tweets for {} users, starting the search'.format(to_finish))
for file in glob.glob(out_path + '/*/tweets.json'):
	p = os.path.abspath(file)
	d = os.path.dirname(p)
	# TODO: make this system indendent
	user = d.split('\\')[-1] # GD windows file system

	with open(p, 'r') as f:
		tweets = json.load(f)

	print("{} tweets to process for user {}".format(len(tweets), user))

	ret = []
	for t in tweets:
		for r in regs:
			if match(t, r):
				# build object
				item = {}
				item['sn'] = user
				item['id'] = t['id']
				item['url'] = build_url(t['id'])
				item['text'] = t['text']
				item['match'] = r.pattern

				ret.append(item)
	
	# write user's tweets to disk
	write_matches(ret, user)
	finished += 1
	print('Finished searching {}/{} users'.format(finished, to_finish))


