from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PaystackRequest, PaystackResponse
from .serializers import PaystackRequestSerializer, PaystackResponseSerializer
from drf_spectacular.utils import extend_schema
import requests
from django.conf import settings

@extend_schema(
    request=PaystackRequestSerializer,
    responses={201: PaystackResponseSerializer}
)
@api_view(['POST'])
def initialize_payment(request):
    serializer = PaystackRequestSerializer(data=request.data)
    if serializer.is_valid():
        paystack_request = serializer.save()
        response_data = initiate_paystack_payment(paystack_request)
        if response_data.get('status'):
            data = response_data['data']
            paystack_response = PaystackResponse.objects.create(
                request=paystack_request,
                authorization_url=data.get('authorization_url', ''),
                access_code=data.get('access_code', ''),
                reference=data.get('reference', ''),
                response_code='200',
                response_description=response_data.get('message', '')
            )
            response_serializer = PaystackResponseSerializer(paystack_response)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_payment(request, reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    return Response(response.json())

def initiate_paystack_payment(paystack_request):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": paystack_request.email,
        "amount": int(paystack_request.amount * 100),  # Paystack uses kobo/cents
        "reference": paystack_request.account_reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
        "metadata": {
            "transaction_desc": paystack_request.transaction_desc
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()