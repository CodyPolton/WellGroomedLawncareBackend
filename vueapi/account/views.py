from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3
from botocore.client import Config
import os
from .models import Yard, Job, JobExpense, Invoice, InvoiceManager, Account
from .serializers import YardSerializer, JobSerializer, JobExpenseSerializer
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
        template = "InvoiceTemplate.docx"
        document = MailMerge(template)
        jobs_history = []
        jobs = request.data['jobs']
        yard = None
        account = None
        accountName = None
        
        total = 0
        invoiceName = 'temp'
        for x in jobs:
            if yard is None:
                yard = Yard.objects.get(pk= x['yard'])    #filter(yardid = x['yard']).values():
                account = Account.objects.get(pk = yard.account_id)                # filter(accountid = yard['account_id']).values():

                accountName = account.f_name + " " + account.l_name
            
            entry_list = list(JobExpense.objects.filter(job= x['jobid']).values())
            for e in entry_list:
                total += e['cost']
                job = {
                    'Qty': '1',
                    'JobAddress': account.address,
                    'Description': e['name'],
                    'UPrice': str(e['cost']),
                    'LinePrice': str(e['cost'])
                }
                jobs_history.append(job)

        
        invoice = Invoice.objects.create_invoice(invoiceName, total, account)
        invoiceName = account.l_name + '_' + account.f_name +  '-' + 'InvoiceID_' + str(invoice.invoiceid) + '.docx'
        invoice.invoice_name = invoiceName
        invoice.save()

        document.merge(
            BillingName = accountName,
            BillingAddress = account.address + '\n' + account.city + ', ' + account.state + ', ' + str(account.zip_code),
            BillingJob = "Mowing",

            AccountName = accountName,

            Date='{:%m-%d-%Y}'.format(date.today()),
            InvoiceId = str(invoice.invoiceid),

            SubTotal = str(total),
            Total = str(total)

        )
        document.merge_rows('Qty', jobs_history)


        document.write('Invoices/' +  invoiceName)

        self.UploadInvoice(invoiceName)

        for x in jobs:
            job = Job.objects.get(pk = x['jobid'])
            job.invoiceid = invoice.invoiceid
            job.invoiced = True
            job.save()
        return Response({'message': "Printed"})
        
    
    def UploadInvoice(self, invoiceName):
        
       
        ACCESS_KEY_ID = 'AKIAZGQ5Y6VBANCPC365'
        ACCESS_SECRET_KEY = '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'
        BUCKET_NAME = 'elasticbeanstalk-us-east-2-632496387394'
        FILE_NAME = 'Invoices/' + invoiceName


        data = open(FILE_NAME, 'rb')

        # S3 Connect
        s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,)
        try:
            response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, str(FILE_NAME), ExtraArgs={'ACL':'public-read'})
            
            print("success")
        except ClientError as e:
            logging.error(e)
            

class OverideInvoice(APIView):

    def post(self, request):
        print(request.FILES['file'])
        files = request.data['file']
        print(files.name)
        file_name = default_storage.save('Invoices/' + files.name, files)

        
        ACCESS_KEY_ID = 'AKIAZGQ5Y6VBANCPC365'
        ACCESS_SECRET_KEY = '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'
        BUCKET_NAME = 'elasticbeanstalk-us-east-2-632496387394'
        FILE_NAME = 'Invoices/' + files.name


        

        # S3 Connect
        s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,)
        try:
            response = s3_client.upload_file(files, BUCKET_NAME, str(FILE_NAME), ExtraArgs={'ACL':'public-read'})
            
            print("success")
        except ClientError as e:
            logging.error(e)

        return Response({'message': "Uploaded"})

    



