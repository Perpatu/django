from django.db import models
from files.models import Files
from departments.models import Departments


class FileQueue(models.Model):
    Queue_id = models.AutoField(primary_key=True)
    File = models.ForeignKey(Files, related_name='Queue_logic', on_delete=models.CASCADE)
    Department = models.ForeignKey(Departments, related_name='Department', on_delete=models.CASCADE)
    Admin_allows = models.BooleanField(default=False)
    User_start = models.BooleanField(default=False)
    User_paused = models.BooleanField(default=False)
    User_end = models.BooleanField(default=False)