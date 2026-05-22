from rest_framework import serializers
from .models import PaystackRequest, PaystackResponse

class PaystackRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaystackRequest
        fields = ['email', 'amount', 'account_reference', 'transaction_desc']

class PaystackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaystackResponse
        fields = '__all__'