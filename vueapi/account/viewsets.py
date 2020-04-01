from rest_framework import viewsets
from .models import Account, Yard, JobType, Job, JobExpenseType, JobExpense, Invoice, EmailTemplates, Crew, Timesheet, PayPeriod
from .serializers import AccountSerializer, YardSerializer, JobTypeSerializer, JobSerializer, JobExpenseSerializer, JobExpenseTypeSerializer, InvoiceSerializer, EmailTemplatesSerializer, CrewSerializer, TimesheetSerializer, PayPeriodSerializer

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

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class EmailTemplatesViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplates.objects.all()
    serializer_class = EmailTemplatesSerializer

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer

class PayPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayPeriod.objects.all()
    serializer_class = PayPeriodSerializer