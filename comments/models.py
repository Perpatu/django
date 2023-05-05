from django.db import models
from users.models import User
from files.models import Files
from projects.models import Project


class CommentsToFile(models.Model):
    Comment_id = models.AutoField(primary_key=True)
    Date_posted = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    File = models.ForeignKey(Files, related_name='comments', on_delete=models.CASCADE)
    Read = models.BooleanField(default=False)
    Text = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return f"Comment {self.Comment_id} by {self.User.username} on: {self.Text}"



class CommentsToProject(models.Model):
    Comment_id = models.AutoField(primary_key=True)
    Date_posted = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    Project = models.ForeignKey(Project, related_name='comments', null=False, on_delete=models.CASCADE)
    Read = models.BooleanField(default=False)
    Text = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return f"Comment {self.Comment_id} by {self.User.username} on: {self.Text}"

"""class CommentsToGroups(models.Model):
    Comment_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_posted = models.DateTimeField(auto_now_add=True)    
    Group_name = models.CharField(max_length=255, null=False)
    Read = models.BooleanField(default=False)
    Comment_text = models.CharField(max_length=255, null=False)"""
