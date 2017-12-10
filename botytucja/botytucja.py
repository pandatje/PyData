# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json
from random import sample
from collections import deque

import tweepy

from .listeners import FollowStreamListener


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


def get_api():
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def get_random_article():
    with open('data/konstytucja.json', 'rt') as f:
        articles = json.loads(f.read())['artykuły']
    number, text = sample(articles.items(), 1)[0]
    return 'Art. %s. %s' % (number, text)


def tweet(text, in_reply_to_status_id=None, api=None):
    if api is None:
        api = get_api()
    return api.update_status(text, in_reply_to_status_id=in_reply_to_status_id)


def tweet_a_random_article():
    api = get_api()
    last_id = None
    for t in tweetsplit(get_random_article()):
        print(t)
        status = tweet(t, in_reply_to_status_id=last_id, api=api)
        last_id = status.id


def get_user_id(handle):
    api = get_api()
    id_str = api.get_user(screen_name=handle).id_str
    print('%s : %s' % (id_str, handle))
    return id_str


def get_user_ids():
    with open('data/users.json') as f:
        users = json.loads(f.read())
    return users.keys()


def follow():
    api = get_api()

    stream_listener = FollowStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    user_ids = get_user_ids()
    print('following %s' %(user_ids))
    stream.filter(follow=user_ids, async=True)


if __name__ == '__main__':
    follow()
