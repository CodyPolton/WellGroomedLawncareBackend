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

#scheduler.add_job(scheduler_jobs.close_timesheets, 'interval', id='Test', seconds=5)
scheduler.add_job(scheduler_jobs.set_payperiod, 'cron', id='Set PayPeriod', day_of_week='2', hour=1 )
#scheduler.add_job(scheduler_jobs.close_timesheets, 'cron', id='Clock out anyone still clocked in', hour=23, minute=59)

scheduler.start()

#========================================