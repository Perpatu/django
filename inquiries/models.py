from django.db import models
from users.models import User


class Inquiry(models.Model):
    Inquiry_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Inquiry_date_created = models.DateField(auto_now=True)
    Inquiry_name = models.CharField(max_length=255)
    Inquiry_content = models.CharField(max_length=10000)
    Comapny_name = models.CharField(max_length=300)
    Inquiry_status = models.CharField(max_length=40, default='new')