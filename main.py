# GoodReads API stuff
from goodreads import client
import re
import urllib
from bs4 import BeautifulSoup

# Twitter API stuff
import tweepy
import random
import os

def cleanedUpQuote(quote):
    #quote = re.sub('<.*?>','',quote)
    p = re.compile(r'<.*?>')
    # select = re.search('authorOrTitle" href="/author/show/1077326.J_K_Rowling', quote)
    # return quote[:select.start()] + quote[select.end():]
    return p.sub('', quote)

# Opens file with Twitter auth keys
with open("secrets.txt") as f:
	secrets = f.readlines()
	# secrets = [consumer key, consumer secret, access token, access secret]
f.close()

# Set Twitter auth info from secrets array, remove \n character
TWITTER_CONSUMER_KEY = secrets[0].rstrip('\n')
TWITTER_CONSUMER_SECRET = secrets[1].rstrip('\n')
TWITTER_ACCESS_TOKEN = secrets[2].rstrip('\n')
TWITTER_ACCESS_SECRET = secrets[3].rstrip('\n')

# Send your auth to Tweepy to access Twitter API
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# Opens file with GoodReads auth keys
with open("goodreads.txt") as gr_file:
	keys = gr_file.readlines()
gr_file.close()

# Set GoodReads auth info
GOODREADS_CONSUMER_KEY = keys[0].rstrip('\n')
GOODREADS_CONSUMER_SECRET = keys[1].rstrip('\n')

# Connect to Good reads client
gc = client.GoodreadsClient(GOODREADS_CONSUMER_KEY, GOODREADS_CONSUMER_SECRET)
gc.authenticate()

goodreads_tag = 'hermione'
#page_num = str(random.randint(1,3))
baseURL = 'https://www.goodreads.com/quotes/tag/'
finalURL = baseURL + goodreads_tag;

# Read URL & parse with BeautifulSoup
html = urllib.urlopen(finalURL).read()
soup = BeautifulSoup(html, 'lxml')
for a in soup.findAll('a'):
	del a['href']

quotes = soup.findAll("div", { "class":"quoteText"})

# Shortcut to image directory
imgdir = os.listdir("img/")

for quotePart in quotes:
	text = str(quotePart)
	matchQuote = re.findall('"(.*)"', text)
	finalQuote = cleanedUpQuote(matchQuote[1])

	if (len(finalQuote) < 136 and finalQuote != 'authorOrTitle'):
		api.update_with_media("img/"+random.choice(imgdir), finalQuote)

	elif (len(finalQuote) >= 136):
		quotes_list = map(str, re.findall('.{100}', finalQuote))
		for quote in quotes_list:
			api.update_with_media("img/"+random.choice(imgdir), quote)
	else:
		print finalQuote

# # Build a list of tweets
# tweetlist = ["If being good at Divination means I have to pretend to see death omens in a lump of tea leaves,", "Im not sure Ill be studying it much longer!",
# "Honestly, am I the only person whos ever bothered to read Hogwarts, A History?",
# "So the Daily Prophet exists to tell people what they want to hear, does it?", 
# "No, Harry, you listen, were coming with you. That was decided months ago years, really."]

# # TWEETS!
# for tweet in tweetlist:
# 	api.update_with_media("img/"+random.choice(imgdir), tweet)