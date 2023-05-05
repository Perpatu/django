from django.contrib import admin
from .models import CommentsToFile, CommentsToProject

class UserAdmin(admin.ModelAdmin):
    list_display = ("Comment_id")
    admin.site.register(CommentsToFile)

class UserAdmin(admin.ModelAdmin):
    list_display = ("Comment_id")
    admin.site.register(CommentsToProject)