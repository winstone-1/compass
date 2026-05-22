from django.db import models

class PaystackRequest(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    transaction_desc = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class PaystackResponse(models.Model):
    request = models.ForeignKey(PaystackRequest, on_delete=models.CASCADE, related_name='responses')
    authorization_url = models.URLField(max_length=500)
    access_code = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    response_code = models.CharField(max_length=10)
    response_description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)