#========================================
# Scheduler Jobs
#========================================
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import pytz
import time
scheduler = BackgroundScheduler()
scheduler.configure(timezone='US/Central')
register_events(scheduler)


# def test_job():
#     time.sleep(4)
#     print("I'm a test job!")

# jobs
import scheduler_jobs

scheduler.add_jobstore(DjangoJobStore(), 'default')
#scheduler.add_job(scheduler_jobs.FirstCronTest, 'interval', seconds=100)

scheduler.add_job(scheduler_jobs.test_job, 'cron', id='Test', hour=18, minute=38 )

scheduler.start()

#========================================