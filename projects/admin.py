from django.contrib import admin
from .models import Project


class UserAdmin(admin.ModelAdmin):
    list_display = ("Project_name")
    admin.site.register(Project)
