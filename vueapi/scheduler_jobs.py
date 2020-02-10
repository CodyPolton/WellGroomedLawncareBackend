from datetime import datetime
from pytz import utc
from account.models import PayPeriod
from datetime import date, datetime, timedelta
import time

def FirstCronTest():
	
	print("I am executed..!")

def test_job():
	start = datetime.now()
	end = datetime.now() + timedelta(days=6)
	print(start.date())
	print(end.date())

def set_payperiod():
	start = datetime.now()
	end = datetime.now() + timedelta(days=6)
	b = PayPeriod(startDate=start, endDate=end)
	b.save()
	print("Set the pay period")