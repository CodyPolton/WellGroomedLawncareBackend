from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3
from botocore.client import Config
import os
from .models import Yard, Job, JobExpense, Invoice, InvoiceManager, Account, EmailTemplates
from .serializers import YardSerializer, JobSerializer, JobExpenseSerializer, InvoiceSerializer
import logging
from botocore.exceptions import ClientError
from datetime import datetime
from mailmerge import MailMerge
from django.core.files.storage import default_storage
from datetime import date , timedelta
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailInvoice(APIView):
    # os.environ['INVOICE_ENV']
    def post(self, request):
        if(not request.data):
            content = {'message': 'Did not receive an Invoice to email'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        invoiceid = request.data.get('invoice')
        invoice = Invoice.objects.get(pk = invoiceid)
        template = None
        if(invoice.invoice_type == 'Mowing'):
            template = EmailTemplates.objects.get(pk = 1)
        elif(invoice.invoice_type == 'Individual'):
            template = EmailTemplates.objects.get(pk = 2)
        subject = template.subject
        account = invoice.account
        receiver_email = ''
        if(os.environ['INVOICE_ENV'] == 'prod/'):
            receiver_email = account.email
        else:
            receiver_email = os.environ['TEST_EMAIL']
            subject = subject + " in prod sends to " + account.email
        if(not invoice.billed):
            account.balance = account.balance + invoice.total_price
            account.save()
        name = account.f_name
        prev = date.today().replace(day=1) - timedelta(days=1)
        month = getMonth(self, prev.month)
        generateEmail(self, receiver_email, name, month,  subject, template.body, invoice.invoice_name)
        invoice.billed = True
        invoice.save()
        content = {'message': 'Invoice has been sent out to ' + name}
        return Response(content, status=status.HTTP_200_OK)

class EmailAllInvoices(APIView):
    def get(self, request):
        invoicesql = 'select * from invoices where approved = true and billed = false'
        
        invoices = Invoice.objects.raw(invoicesql)
        if(not invoices):
            content = {'message': 'No invoices to email'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        for invoice in invoices:
            print(invoice.invoice_name)
            template = None
            if(invoice.invoice_type == 'Mowing'):
                template = EmailTemplates.objects.get(pk = 1)
            elif(invoice.invoice_type == 'Individual'):
                template = EmailTemplates.objects.get(pk = 2)
            subject = template.subject
            account = invoice.account
            receiver_email = ''
            if(os.environ['INVOICE_ENV'] == 'prod/'):
                receiver_email = account.email
            else:
                receiver_email = os.environ['TEST_EMAIL']
                subject = subject + " in prod sends to " + account.email
            name = account.f_name
            prev = date.today().replace(day=1) - timedelta(days=1)
            month = getMonth(self, prev.month)
            if(not invoice.billed):
                account.balance = account.balance + invoice.total_price
                account.save()
            print(receiver_email)
            generateEmail(self, receiver_email, name, month,  subject, template.body, invoice.invoice_name)
            invoice.billed = True
            invoice.save()
        
        
        content = {'message': 'Invoices have been sent out'}
        return Response(content, status=status.HTTP_200_OK)



class TestTemplate(APIView):

    def get(self,request):
        id = request.GET.get('code', '0')
        sender_email = os.environ['SENDER_EMAIL']
        password = os.environ['SENDER_PASSWORD']
        receiver_email = os.environ['TEST_EMAIL']
        name = "TestName"
        month = "TestMonth"
        logo = "Images/logo.png"
        template = EmailTemplates.objects.get(pk = id)
        subject = template.subject
        tempbody = template.body
        tempbody = tempbody.replace("$Name", name)
        tempbody = tempbody.replace('$Month', month)
        body = """\
        <html>
            <body>
                <p style='font-family:"Comic Sans MS", cursive, sans-serif; font-size: 16px;'>Hi """ + name + """,<br><br> """ + tempbody + """
                <br><br>Landon Wiswall<br>
                Well-Groomed Lawn Care, LLC<br>
                </p>
            </body>
        </html>
        """ 
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        # Add body to email
        message.attach(MIMEText(body, "html"))

        fp = open(logo, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        content = {'message': 'Test email has been sent out'}
        return Response(content, status=status.HTTP_200_OK)

def getMonth(self, month):
    if(month == 1):
        return "January"
    elif(month == 2):
        return "February"
    elif(month == 3):
        return "March"
    elif(month == 4):
        return "April"
    elif(month == 5):
        return "May"
    elif(month == 6):
        return "June"
    elif(month == 7):
        return "July"
    elif(month == 8):
        return "August"
    elif(month == 9):
        return "September"
    elif(month == 10):
        return "October"
    elif(month == 11):
        return "November"
    elif(month == 12):
        return "December"

def generateEmail(self, receiver_email, name, month, subject, tempbody, filename):
    sender_email = os.environ['SENDER_EMAIL']
    password = os.environ['SENDER_PASSWORD']
    logo = "Images/logo.png"
    tempbody = tempbody.replace("$Name", name)
    tempbody = tempbody.replace('$Month', month)
    body = """\
    <html>
        <body>
            <p style='font-family:"Comic Sans MS", cursive, sans-serif; font-size: 16px;'>Hi """ + name + """,<br><br> """ + tempbody + """
            <br><br>Landon Wiswall<br>
            Well-Groomed Lawn Care, LLC<br>
            </p>
        </body>
    </html>
    """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "html"))

    path = os.environ['INVOICE_ENV'] + 'Invoices/' + filename

    with default_storage.open(path) as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment; filename={}".format(filename),
    )

    fp = open(logo, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    message.attach(part)

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
