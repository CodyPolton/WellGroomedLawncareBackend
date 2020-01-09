from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Yard, Job, JobExpense
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
        


