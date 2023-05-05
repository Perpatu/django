from django.db import models


class Client(models.Model):
    Client_id = models.AutoField(primary_key=True)
    Client_name = models.CharField(max_length=255, unique=True)
    Phone_number = models.CharField(max_length=15, blank=True)
    Email = models.CharField(max_length=100, blank=True)
    Address = models.CharField(max_length=255, blank=True)
    Date_add = models.DateField(auto_now_add=True)
    Color = models.CharField(max_length=50, null=True)

    
    def __str__(self) -> str:
        return self.Client_name