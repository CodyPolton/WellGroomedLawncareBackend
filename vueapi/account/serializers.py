from rest_framework import serializers
from .models import Account, Yard, JobType, Job, JobExpenseType, JobExpense
class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)
        
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class YardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yard
        fields = '__all__'
        
class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExpenseType
        fields = '__all__'

class JobExpenseSerializer(PatchModelSerializer):
    class Meta:
        model = JobExpense
        fields = '__all__'


