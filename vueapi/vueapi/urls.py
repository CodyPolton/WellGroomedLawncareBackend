"""vueapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from .routers import router
from account import views, invoiceviews, emailviews, timesheetviews

from rest_framework_simplejwt import views as jwt_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.authtoken.views import obtain_auth_token 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include(router.urls)),
    url('api/accountsyards', views.YardsOfAccount.as_view()),
    url('api/yardjobs', views.JobsOfYard.as_view()),
    url('api/expensesofjob', views.ExpensesOfJob.as_view()),
    url('api/yardmowedcheck', views.YardMowedCheck.as_view()),
    url('api/yardforcrew', views.YardForCrew.as_view()),
    # url('api/upload', views.uploadFile.as_view()),
    url('api/generateinvoice', invoiceviews.GenerateInvoice.as_view()),
    url('api/overideinvoice', invoiceviews.OverideInvoice.as_view()),
    url('api/invoicejobs', invoiceviews.InvoiceJobs.as_view()),
    url('api/accountinvoices', invoiceviews.AccountInvoices.as_view()),
    url('api/deleteinvoice', invoiceviews.DeleteInvoice.as_view()),
    url('api/mowinginvoices', invoiceviews.GenerateMowingInvoices.as_view()),
    url('api/emailinvoice', emailviews.EmailInvoice.as_view()),
    url('api/testtemplate', emailviews.TestTemplate.as_view()),
    url('api/emailallinvoices', emailviews.EmailAllInvoices.as_view()),
    url('api/clockinstatus', timesheetviews.ClockinStatus.as_view()),
    url('api/gettimesheet', timesheetviews.GetTimesheet.as_view()),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/', obtain_jwt_token),
    url(r'^api/token/refresh/', refresh_jwt_token),
    url('api/returnuserdetails', views.ReturnUserDetails.as_view()),
    


]

import execute


