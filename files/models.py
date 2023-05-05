from django.db import models
from os.path import join
from projects.models import Project
from users.models import User
from departments.models import Departments
from inquiries.models import Inquiry


class Files(models.Model):
    def file_dir(self, filename):
        return join(str(self.Project.Project_id), filename)
    
    File_id = models.AutoField(primary_key=True)
    Project = models.ForeignKey(Project, related_name='Files', on_delete=models.CASCADE)    
    User = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    Queue = models.ManyToManyField(Departments, blank=True)    
    File_destiny = models.CharField(max_length=30, null=False)
    File_date_created = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to=file_dir) 
    filename = models.CharField(max_length=255)
    File_new = models.BooleanField(default=True)
    File_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.filename
    

class FilesInquiry(models.Model):
    def file_dir(self, filename):        
        return join('Inquiry_' + str(self.Inquiry.Inquiry_id), filename)
    
    File_id = models.AutoField(primary_key=True)
    Inquiry = models.ForeignKey(Inquiry, related_name='Files', on_delete=models.CASCADE)       
    File_date_created = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to=file_dir) 
    filename = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.filename