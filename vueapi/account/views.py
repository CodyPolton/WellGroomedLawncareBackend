from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
import boto3
from botocore.client import Config
import os
from .models import Yard, Job, JobExpense, Invoice, InvoiceManager, Account
from .serializers import YardSerializer, JobSerializer, JobExpenseSerializer, InvoiceSerializer
import logging
from botocore.exceptions import ClientError
from datetime import datetime
from mailmerge import MailMerge
from django.core.files.storage import default_storage
from datetime import date

logger = logging.getLogger(__name__)

# Create your views here.

class YardsOfAccount(APIView):

    def get(self, request):
        id = request.GET.get('id', '0')
        yards = Yard.objects.filter(account=id)
        logger.error(yards)
        serializer = YardSerializer(yards, many=True)
        if yards is None:
            return Response({"message": "Hello, world! " + id})
        
        else:
           return Response(serializer.data) 


class JobsOfYard(APIView):

    def get(self,request):
        id = request.GET.get('yardid', '0')
        jobs = Job.objects.filter(yard=id)
        logger.info(jobs)
        serializer = JobSerializer(jobs, many=True)
        if jobs is None:
            return Response({"message": "No jobs " + id})

        else:
           return Response(serializer.data) 

class ExpensesOfJob(APIView):

    def get(self,request):
        id = request.GET.get('jobid', '0')
        expenses = JobExpense.objects.filter(job=id)
        logger.info(expenses)
        serializer = JobExpenseSerializer(expenses, many=True)
        if expenses is None:
            return Response({"message": "No expenses " + id})

        else:
           return Response(serializer.data) 

class YardMowedCheck(APIView):
    
    def get(self,request):
        yardid = request.GET.get('yardid', '0')
        now = datetime.now()
        if yardid == '0':
            return Response({"message": "Need yardid to process"})
        else: 
            jobs = Job.objects.filter(yard_id=yardid, date_created__date=datetime.date(now), job_type='Mowing')
            serializer = JobSerializer(jobs, many=True)
            if not jobs:
                return Response({'message': "Hasn't been mowed today"})
            else: 
                return Response({'message': "Mowed today"})

class YardForCrew(APIView):

    def get(self,request):
        crewid = request.GET.get('crew', '0')
        if crewid == '0':
            return Response({"message": "Need crew to process"})
        else: 
            yards = Yard.objects.filter(crew=crewid)
            serializer = YardSerializer(yards, many=True)
            if not yards:
                return Response({'message': "No yards for crew" + crewid})
            else: 
                return Response(serializer.data) 

class ReturnUserDetails(APIView):

    def post(self,request):
        token = Token.objects.get(key=request.data.get('token'))
        group = Group.objects.get(user= token.user_id)
        return Response({'group_level': group.id, 'first_name': token.user.first_name, 'last_name': token.user.last_name, 'group_name': group.name, 'user_id' : token.user.id})
        

# class uploadFile(APIView):

#     def get(self, request):
#         test = os.environ['TEST']
#         print(test)
#         ACCESS_KEY_ID = 
#         ACCESS_SECRET_KEY = 
#         BUCKET_NAME = 
#         FILE_NAME = 'InvoiceTemplate.docx';


#         data = open(FILE_NAME, 'rb')

#         # S3 Connect
#         s3 = boto3.resource(
#             's3',
#             aws_access_key_id=ACCESS_KEY_ID,
#             aws_secret_access_key=ACCESS_SECRET_KEY,
#             config=Config(signature_version='s3v4')
#         )

#         # Image Uploaded
#         s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')

#         print ("Done")
#         return Response({'message': "Uploaded"})

