from django.contrib import admin
from .models import Files

class UserAdmin(admin.ModelAdmin):
    list_display = ("filename")
    admin.site.register(Files)