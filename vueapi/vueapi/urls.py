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
from account import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url('api/accountsyards', views.YardsOfAccount.as_view()),
    url('api/yardjobs', views.JobsOfYard.as_view()),
    url('api/expensesofjob', views.ExpensesOfJob.as_view()),
    url('api/yardmowedcheck', views.YardMowedCheck.as_view()),
    # url('api/upload', views.uploadFile.as_view()),
    url('api/generateinvoice', views.GenerateInvoice.as_view()),
    url('api/overideinvoice', views.OverideInvoice.as_view()),
    url('api/invoicejobs', views.InvoiceJobs.as_view()),
    url('api/accountinvoices', views.AccountInvoices.as_view()),
    url('api/deleteinvoice', views.DeleteInvoice.as_view())

]


