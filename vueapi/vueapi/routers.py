from rest_framework import routers
from account.viewsets import AccountViewSet, YardViewSet, JobTypeViewSet, JobViewSet, JobExpenseViewSet, JobExpenseTypeViewSet, InvoiceViewSet
from account import views

router = routers.DefaultRouter()
router.register(r'account', AccountViewSet)
router.register(r'yard', YardViewSet) 
router.register(r'jobtype', JobTypeViewSet)
router.register(r'job', JobViewSet)
router.register(r'jobexpensetype', JobExpenseTypeViewSet)
router.register(r'jobexpense', JobExpenseViewSet)
router.register(r'invoice', InvoiceViewSet)