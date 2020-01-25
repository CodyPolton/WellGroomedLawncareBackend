from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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

class GenerateInvoice(APIView):

    def post(self, request):
        template = "InvoiceTemplate.docx"
        document = MailMerge(template)
        jobs_history = []
        jobs = request.data.get('jobs')
        if jobs is None: 
            content = {'message': 'No Jobs sent to backend'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        yard = None
        account = None
        accountName = None
        
        total = 0
        invoiceName = 'temp'
        for x in jobs:
            if yard is None:
                yard = Yard.objects.get(pk= x['yard'])    
                account = Account.objects.get(pk = yard.account_id)               

                accountName = account.f_name + " " + account.l_name
            
            entry_list = list(JobExpense.objects.filter(job= x['jobid']).values())
            i = 1
            for e in entry_list:
                total += e['cost']
                if i == 1:
                    job = {
                        'JobAddress': account.address,
                        'Description': e['description'],
                        'DateCompleted': x['date_completed']

                    }
                    i = 2
                else: 
                    job = {
                        'Description': e['description'],
                    }
                jobs_history.append(job)

        
        invoice = Invoice.objects.create_invoice(invoiceName, total, account)
        invoiceName = account.l_name + '_' + account.f_name +  '-' + 'InvoiceID_' + str(invoice.invoiceid) + '.docx'
        invoice.invoice_name = invoiceName
        

        document.merge(
            BillingName = accountName,
            BillingAddress = account.address + '\n' + account.city + ', ' + account.state + ', ' + str(account.zip_code),

            AccountName = accountName,

            Date='{:%m-%d-%Y}'.format(date.today()),
            InvoiceId = str(invoice.invoiceid),

            SubTotal = str(total),
            Total = str(total)

        )
        document.merge_rows('Description', jobs_history)


        document.write('tmp/' +  invoiceName)

        self.UploadInvoice(invoiceName)

        invoice.save()

        for x in jobs:
            job = Job.objects.get(pk = x['jobid'])
            job.invoiceid = invoice.invoiceid
            job.invoiced = True
            job.save()
        return Response({'message': "Printed"})
        
    
    def UploadInvoice(self, invoiceName):
        
        FILE_NAME = os.environ['INVOICE_ENV'] + 'Invoices/' + invoiceName
        data = open('tmp/' + invoiceName, 'rb')
        file_name = default_storage.save(FILE_NAME, data)
        os.remove('tmp/' + invoiceName)


class GenerateMowingInvoices(APIView):

    def get(self, request):
        month = request.GET.get('month')
        jobsql = ("select distinct j.* from accounts acc "
                "inner join yards y on acc.accountid = y.account_id "
                "inner join jobs j on j.yard_id = y.yardid " 
                "where job_type = 'Mowing' " 
                "and j.invoiced = false " 
                "and EXTRACT(Month from date_completed) = " + month + 
                " ORDER BY j.account_id desc")
        jobs = Job.objects.raw(jobsql)
        if(not jobs):
            content = {'message': 'No Jobs to invoice.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        for x in range(jobs[0].account_id + 1):
            print("x = " + str(x))
            accountJobs = []
            for job in jobs:
                if(job.account_id == x):
                    accountJobs.append(job)
            
            account = None
            jobs_history = []
            total = 0
            if(len(accountJobs) > 0):
                template = "MowingInvoiceTemplate.docx"
                document = MailMerge(template)
                account = Account.objects.get(pk = x)
                accountName = account.f_name + " " + account.l_name
                print(accountName)
                for job in accountJobs:
                    yardJobs = []
                    if(not job.invoiced):
                        yardJobs.append(job)
                        job.invoiced = True
                        yard = Yard.objects.get(pk = job.yard_id)
                        
                        for x in accountJobs: 
                            if(x.yard_id == job.yard_id and not x.invoiced):
                                x.invoiced = True
                                yardJobs.append(x)
                        print("---------------")
                        mowedCounter = 0
                        mowDescription = "Mowed on "
                        for yjob in yardJobs:
                            print(yjob.name)
                            if(yjob.name == 'Mow(Auto)'):
                                mowDescription += str(yjob.date_completed.strftime("%m/%d")) + ", "
                                mowedCounter = mowedCounter + 1
                            else: 
                                print("in else")
                                print(yjob.name)
                                entry_list = list(JobExpense.objects.filter(job= yjob.jobid).values())
                                for e in entry_list:
                                    total += e['cost']
                                    job = {
                                        'Qty': '1',
                                        'JobAddress': yard.address,
                                        'Description': e['description'],
                                        'UPrice': str(e['cost']),
                                        'LinePrice': str(e['cost'])
                                    }
                                    jobs_history.append(job)
                        mowjobs = None
                        if(mowedCounter != 0):
                            linePrice = mowedCounter*yard.mow_price
                            total += linePrice
                            mowjobs = {
                                'Qty': str(mowedCounter),
                                'JobAddress': yard.address,
                                'Description': mowDescription[:-2],
                                'UPrice': str(yard.mow_price),
                                'LinePrice': str(linePrice)
                            }
                            print(mowjobs)
                            jobs_history.append(mowjobs)
                            print(jobs_history)
        
                            
                invoiceName = 'temp'
                invoice = Invoice.objects.create_invoice(invoiceName, total, account)
                invoiceName = account.l_name + '_' + account.f_name +  '-' + 'InvoiceID_' + str(invoice.invoiceid) + '.docx'
                invoice.invoice_name = invoiceName

                print(invoiceName)


                document.merge(
                    BillingName = accountName,
                    BillingAddress = account.address + '\n' + account.city + ', ' + account.state + ', ' + str(account.zip_code),
                    BillingJob = "Mowing, edging along sidewalks, weed eating and blowing off property (includes picking up and trash on lawn)",

                    AccountName = accountName,

                    Date='{:%m-%d-%Y}'.format(date.today()),
                    InvoiceId = str(invoice.invoiceid),

                    SubTotal = str(total),
                    Total = str(total)
                )
                document.merge_rows('Qty', jobs_history)

                document.write('tmp/' +  invoiceName)

                self.UploadInvoice(invoiceName)

                invoice.save()

            for x in accountJobs:
                job = Job.objects.get(pk = x.jobid)
                job.invoiceid = invoice.invoiceid
                job.invoiced = True
                job.save()

        return Response({'message': "Printed"})


    def UploadInvoice(self, invoiceName):
        
        FILE_NAME = os.environ['INVOICE_ENV'] + 'Invoices/' + invoiceName
        data = open('tmp/' + invoiceName, 'rb')
        file_name = default_storage.save(FILE_NAME, data)
        os.remove('tmp/' + invoiceName)       
            

class OverideInvoice(APIView):

    def post(self, request):
        files = request.data['file']
        id = request.data['id']
        invoice = Invoice.objects.get(pk=id)
        print(invoice)
        if invoice is not None: 
            default_storage.delete(os.environ['INVOICE_ENV'] + 'Invoices/' + invoice.invoice_name)
            fileName = files.name[:-5] + '_' + files.name[-5:]
            print(fileName)
            file_names = default_storage.save(os.environ['INVOICE_ENV'] + 'Invoices/' + fileName, files)
            invoice.invoice_name = fileName
            invoice.save()
            return Response({'message': "Uploaded"})

        

        content = {'message': 'Invoice not found in database with id of ' + id}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

class DeleteInvoice(APIView):

    def get(self,request):
        invoiceid = request.GET.get('invoiceid', '0')
        invoice = Invoice.objects.get(pk=invoiceid)
        print(invoice.invoiceid)
        if invoice is not None:
            default_storage.delete(os.environ['INVOICE_ENV'] + 'Invoices/' + invoice.invoice_name)
            invoice.delete()
            content = {'message': 'Invoice successfully deleted'}
            return Response(content, status=status.HTTP_200_OK)
        else: 
            content = {'message': 'Invoice not found in database with id of ' + invoiceid}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class InvoiceJobs(APIView):

    def get(self, request):
        id = request.GET.get('invoiceid', '0')
        jobs = Job.objects.filter(invoiceid=id)
        logger.info(jobs)
        serializer = JobSerializer(jobs, many=True)
        if jobs is None:
            return Response({"message": "No jobs " + id})

        else:
           return Response(serializer.data) 
    
class AccountInvoices(APIView):
    def get(self, request):
        id = request.GET.get('id', '0')
        invoices = Invoice.objects.filter(account=id)
        logger.info(invoices)
        serializer = InvoiceSerializer(invoices, many=True)
        if invoices is None:
            return Response({"message": "No invoices for id = " + id})

        else:
           return Response(serializer.data)

