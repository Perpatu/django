from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=255)    
    role = models.CharField(max_length=30, blank=True)    
    phone_number = models.CharField(max_length=9, blank=True)
    department = models.CharField(max_length=25, blank=True)   
    own_description = models.CharField(max_length=2000, blank=True)
    boss_description = models.CharField(max_length=2000, blank=True)
    education = models.CharField(max_length=2000, blank=True)
    experience = models.CharField(max_length=5000, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
