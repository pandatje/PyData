# -*- coding: utf-8 -*-
from __future__ import print_function

import tweepy


class FollowStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False
