from rest_framework import serializers
from .models import * 

class ContractRequestLoggerSerializer(serializers.ModelField):

    class Meta:
        model = ContractRequestLogger