from rest_framework import viewsets
from .models import Account, Yard, JobType, Job, JobExpenseType, JobExpense
from .serializers import AccountSerializer, YardSerializer, JobTypeSerializer, JobSerializer, JobExpenseSerializer, JobExpenseTypeSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class YardViewSet(viewsets.ModelViewSet):
    queryset = Yard.objects.all()
    serializer_class = YardSerializer

class JobTypeViewSet(viewsets.ModelViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = JobExpenseType.objects.all()
    serializer_class = JobExpenseTypeSerializer

class JobExpenseViewSet(viewsets.ModelViewSet):
    queryset = JobExpense.objects.all()
    serializer_class = JobExpenseSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)