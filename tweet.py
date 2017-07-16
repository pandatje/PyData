import os
from pprint import pprint
from random import sample
from collections import deque

import tweepy


MAX_TWEET = 140
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
        while words and len(tweet) + len(words[0]) + 1 <= 137:
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
    with open('constitution.txt', 'rt') as f:
        text = f.read()
    text = text.split('Art.')[1:]
    return sample(text, 1)[0].strip()


def main():
    last_id = None
    for t in tweetsplit(get_random_article()):
        print(t)
        status = tweet(t, in_reply_to_status_id=last_id)
        last_id = status.id


if __name__ == '__main__':
    main()
