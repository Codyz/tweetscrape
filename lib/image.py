import io
import os
import sys
import wget
import glob
import json
from pathlib import Path
from google.cloud import vision
from google.cloud.vision import types

# create client
client = vision.ImageAnnotatorClient()
dir_path = os.path.dirname(os.path.abspath(__file__))
out_path = dir_path + '/../out/'
out_folder = Path(dir_path)


# download one image from twitter
# @param url of the image to download
# @param username of user
# @param String tweet_id this will be the file name 
def download(url, username, tweet_id):
	local_file = (out_folder / username) / tweet_id
	wget.download(url, local_file)


# extract image urls from tweet objects
# @param tweet Tweet
# @param username
# @returns Array{info{url, id, image_id, username}}
def extract(tweets, username):
	ret = []
	for t in tweets:
		media = t['entities'].get('media', [])
		for m in media:
			if m['type'] == 'photo':
				item = {}
				item['id'] = str(m['id'])
				item['tweet_id'] = str(t['id'])
				item['username'] = username
				item['url'] = m['media_url']

				ret.append(item)

	return ret

# label the image
# @param file String path to image file
# @returns List{String} list of image labels, ignore topicality scores
def label(file):
	with open(dir_path + '/../' + file, 'rb') as f:
		img = f.read()

	img = types.Image(content = img)

	res = client.label_detection(image = img)
	labels = res.label_annotations
	print(labels)
	# labels = [l['description'] for l in labels]
	# return labels


# get all cz images
for file in glob.glob(out_path + '/*/tweets.json'):
	p = os.path.abspath(file)
	d = os.path.dirname(p)
	# TODO: make this system indendent
	split_on = '\\' if sys.platform == 'win32' else '/'
	user = d.split(split_on)[-1] # GD windows file system

	with open(p, 'r', encoding = 'utf8') as f:
		tweets = json.load(f)

	print("{} tweets to process for user {}".format(len(tweets), user))
	images = extract(tweets, user)
	print("{} images found".format(len(images)))