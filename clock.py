import os

from apscheduler.schedulers.blocking import BlockingScheduler

from botytucja import tweet_a_random_article


TWEET_INTERVAL_MINUTES = os.environ.get('TWEET_INTERVAL_MINUTES', 60 * 6)


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=TWEET_INTERVAL_MINUTES)
def timed_job():
    tweet_a_random_article()


sched.start()
