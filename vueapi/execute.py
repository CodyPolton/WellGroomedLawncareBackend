#========================================
# Scheduler Jobs
#========================================
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from pytz import utc
import time
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)
register_events(scheduler)

@register_job(scheduler, "interval", seconds=10)
def test_job():
    time.sleep(4)
    print("I'm a test job!")

# jobs
import scheduler_jobs

scheduler.add_job(scheduler_jobs.FirstCronTest, 'interval', seconds=100)
scheduler.add_job(test_job, 'interval', seconds=10, id='test_job')
scheduler.add_jobstore(DjangoJobStore(), 'deafault')
scheduler.start()

#========================================