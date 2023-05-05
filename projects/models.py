from django.db import models
from users.models import User
from clients.models import Client 


class Project(models.Model):
    Project_id = models.AutoField(primary_key=True)   
    Project_group = models.ManyToManyField(User, related_name='Group', blank=True) 
    User = models.ForeignKey(User, related_name='manager', on_delete=models.CASCADE)    
    Client = models.ForeignKey(Client, related_name='client', on_delete=models.CASCADE)    
    Project_name = models.CharField(max_length=100)
    Project_date_created = models.DateField(null=False)
    Project_date_modified = models.DateTimeField(auto_now=True)
    Project_end_date = models.DateField(null=False)
    Project_progress = models.IntegerField(default=0)
    Project_priority = models.CharField(max_length=20)
    Project_status = models.CharField(max_length=20, default='In design')
    Project_number = models.CharField(max_length=255, null=False)    
    Project_secretariat = models.BooleanField(default=False)
    Project_invoice = models.CharField(max_length=21, default='NO')
    Project_or_order = models.CharField(max_length=20)    
    Project_order_number = models.CharField(max_length=255, blank=True)
    Project_message = models.BooleanField(default=False)
    Project_copy = models.BooleanField(max_length=255, default=False)
    Project_copy_status = models.BooleanField(default=False)
    Project_copy_file_status = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.Project_name