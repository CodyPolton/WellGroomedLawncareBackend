from rest_framework import routers
from account.viewsets import AccountViewSet, YardViewSet, JobTypeViewSet, JobViewSet, JobExpenseViewSet, JobExpenseTypeViewSet, InvoiceViewSet, EmailTemplatesViewSet, CrewViewSet, TimesheetViewSet, PayPeriodViewSet
from account import views

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)
router.register(r'yard', YardViewSet) 
router.register(r'jobtype', JobTypeViewSet)
router.register(r'job', JobViewSet)
router.register(r'jobexpensetype', JobExpenseTypeViewSet)
router.register(r'jobexpense', JobExpenseViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'emailtemplates', EmailTemplatesViewSet)
router.register(r'payperiod', PayPeriodViewSet)
router.register(r'timesheet',TimesheetViewSet)
router.register(r'crew', CrewViewSet)