from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3
from botocore.client import Config
import os
from .models import Yard, Job, JobExpense, Invoice
from .serializers import YardSerializer, JobSerializer, JobExpenseSerializer
import logging
from datetime import datetime

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

class uploadFile(APIView):

    def get(self, request):

        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        ACCESS_KEY_ID = 'AKIAZGQ5Y6VBANCPC365'
        ACCESS_SECRET_KEY = '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'
        BUCKET_NAME = 'elasticbeanstalk-us-east-2-632496387394'
        FILE_NAME = 'InvoiceTemplate.docx';


        data = open(FILE_NAME, 'rb')

        # S3 Connect
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )

        # Image Uploaded
        s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')

        print ("Done")
        # invoicefile = 'InvoiceTemplate.docx'
        # upload = Invoice(invoice = invoicefile)
        # upload.save()
        return Response({'message': "Uploaded"})

class GenerateInvoice(APIView):

    def post(self, request):
        print(request.POST.getlist('selected'))
        return Response({'message': "Printed"})
        


