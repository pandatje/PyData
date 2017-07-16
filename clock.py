from apscheduler.schedulers.blocking import BlockingScheduler

from tweet import tweet_a_random_article


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    tweet_a_random_article()


sched.start()
