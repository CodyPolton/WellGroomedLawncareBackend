from datetime import datetime
from pytz import utc
from account.models import PayPeriod, Timesheet
from datetime import date, datetime, timedelta, time

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

# def close_timesheets():
# 	print('timesheets')
# 	opentimesheets = Timesheet.objects.filter(end_time = None)
# 	now = datetime.now().time()
# 	time = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
# 	print(time)
# 	for timesheet in opentimesheets:

# 		timesheet.end_time = time
# 		hours = (datetime.strptime(str(timesheet.end_time),'%H:%M:%S') - datetime.strptime(str(timesheet.start_time),'%H:%M:%S'))
# 		print(hours)
# 		#timesheet.save()