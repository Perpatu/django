from django.db import models
from django.core.validators import MinValueValidator

class StaticDepartments(models.Model):
    def static():
        return {'Delete': 1, 'File': 2, 'filename': 3}
    
    Static_id = models.AutoField(primary_key=True)
    Departments_static_name = models.JSONField(default=static)


class Departments(models.Model):
    Departments_id = models.AutoField(primary_key=True)        
    Departments_name = models.CharField(max_length=255, blank=True, unique=True)
    Departments_order = models.IntegerField(unique=True, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return self.Departments_name