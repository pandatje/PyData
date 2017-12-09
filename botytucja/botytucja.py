import os
import json
from pprint import pprint
from random import sample
from collections import deque

import tweepy


MAX_TWEET = 280
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', None)
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', None)
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', None)


def tweetsplit(text):
    words = deque(w.strip() for w in text.split())
    tweets = []
    done = False

    while not done:
        tweet = ''
        while words and len(tweet) + len(words[0]) + 1 <= (MAX_TWEET - 3):
            tweet += words.popleft() + ' '
            if not words:
                done = True
        tweet = tweet.strip()
        if not done:
            tweet += '...'
        tweets.append(tweet)
    return tweets


def tweet(text, in_reply_to_status_id=None):
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api.update_status(text, in_reply_to_status_id=in_reply_to_status_id)


def get_random_article():
    with open('constitution.json', 'rt') as f:
        articles = json.loads(f.read())['artykuły']
    number, text = sample(articles.items(), 1)[0]
    return f'Art. {number}. {text}'


def tweet_a_random_article():
    last_id = None
    for t in tweetsplit(get_random_article()):
        print(t)
        status = tweet(t, in_reply_to_status_id=last_id)
        last_id = status.id


if __name__ == '__main__':
    tweet_a_random_article()
