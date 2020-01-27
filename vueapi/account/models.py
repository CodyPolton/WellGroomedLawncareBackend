from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator

# Create your models here.
class Account(models.Model):
    accountid = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    phone_no = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    auto_invoice = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'accounts'
        ordering = ['-accountid']

class Yard(models.Model):
    yardid = models.AutoField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    mow_price = models.DecimalField( max_digits=6, decimal_places=2, null=True)
    scheduled = models.BooleanField(default = False)
    crew = models.CharField(max_length=2, blank=True)
    days = ArrayField(
            models.CharField(max_length=6, default='None'),
            size=4,
            default=list,

    )
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'yards'
        ordering = ['-yardid']

class JobType(models.Model):
    job_typeid = models.AutoField(primary_key=True)
    job_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'job_types'
        ordering = ['job_typeid']

class Job(models.Model):
    jobid = models.AutoField(primary_key=True)
    yard = models.ForeignKey('Yard', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=255)
    date_completed = models.DateField(null=True)
    job_total = models.DecimalField( max_digits=10, decimal_places=2, null=True)
    invoiced = models.BooleanField(default = False)
    invoiceid = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-jobid']

class JobExpenseType(models.Model):
    job_expense_typeid = models.AutoField(primary_key=True)
    job_expense_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'job_expense_types'
        ordering = ['job_expense_typeid']

class JobExpense(models.Model):
    job_expenseid = models.AutoField(primary_key=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    job_expense_type = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'job_expense'
        ordering = ['-job_expenseid']

class InvoiceManager(models.Manager):
    def create_invoice(self, name, total, accountid, Itype):
        invoice = self.create(invoice_name=name, total_price=total, account=accountid, invoice_type=Itype)
        return invoice

class Invoice(models.Model):
    invoiceid = models.AutoField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_name = models.CharField(max_length=255)
    invoice_type = models.CharField(max_length=255)
    paid = models.BooleanField(default = False)
    billed = models.BooleanField(default = False)
    approved = models.BooleanField(default = False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    objects = InvoiceManager()

    class Meta:
        db_table = 'invoices'
        ordering = ['-invoiceid']

class EmailTemplates(models.Model):
    templateid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    
    class Meta:
        db_table = 'email_templates'
        ordering = ['templateid']

class Crew(models.Model):
    crewid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    crew_lead = models.CharField(max_length=255, blank=True)






