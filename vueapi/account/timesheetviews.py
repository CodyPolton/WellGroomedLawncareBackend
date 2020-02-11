from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
import boto3
import jsons
from botocore.client import Config
import os
from .models import Yard, Job, JobExpense, Invoice, InvoiceManager, Account, Timesheet, PayPeriod
from .serializers import YardSerializer, JobSerializer, JobExpenseSerializer, InvoiceSerializer, PayPeriodSerializer, TimesheetSerializer
import logging
from botocore.exceptions import ClientError
from datetime import datetime
from mailmerge import MailMerge
from django.core.files.storage import default_storage
from datetime import date

logger = logging.getLogger(__name__)

class ClockinStatus(APIView):

    def get(self, request):
        userid = request.GET.get('userid', '0')
        status = None
        now = datetime.now()
        timesheet = Timesheet.objects.filter(userid = userid, date_created__date=datetime.date(now))
        payperiod = PayPeriod.objects.all().first()
        if not timesheet:
            status = 'No Entry'
            serializer = PayPeriodSerializer(payperiod, many=False)
            return Response({'status': status, 'payperiod': serializer.data})
        else:
            print(timesheet[0].timesheetid)
            status = timesheet[0].status
            tsserializer = TimesheetSerializer(timesheet, many=True)
            serializer = PayPeriodSerializer(payperiod, many=False)
            return Response({'status': status, 'timesheet': tsserializer.data, 'payperiod': serializer.data})

class GetTimesheet(APIView):
    
    def post(self, request):
        userid = request.data.get('userid')
        payperiod = PayPeriod.objects.all().first()
        weektimesheet = Timesheet.objects.filter(userid = userid, payperiodid = payperiod.payperiodid)
        tsserializer = TimesheetSerializer(weektimesheet, many=True)
        print(weektimesheet)
        if not weektimesheet:
            return Response({'status': 'None'})
        else:
            return Response({'timesheet': tsserializer.data, 'status': 'Timesheets'})
