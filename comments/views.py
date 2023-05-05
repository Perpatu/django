from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.core.cache import cache

from .models import CommentsToFile, CommentsToProject
from .serializers import CommentsToFilePostSerializer, CommentsToProjectPostSerializer


class FileCommentsPostView(APIView):
    #permission_classes = [IsAuthenticated,]
    def post(self, request, project_id):
        comment_data = JSONParser().parse(request)
        comment_serializer = CommentsToFilePostSerializer(data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            cache.delete('file_project_'+ str(project_id))
            cache.delete('file_project_admin_' + str(project_id))
            cache.delete('file_secretariat_' + str(project_id))
            cache.delete('file_shop_' + str(project_id))
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response("Added Successfully!!")        
        return Response("Failed to Add")


class ComentFileDeleteView(APIView):
    def delete(self, request, id=0, project_id=0):
        comment = CommentsToFile.objects.get(Comment_id=id)        
        comment.delete()
        cache.delete('file_project_'+ str(project_id))
        cache.delete('file_project_admin_' + str(project_id))
        cache.delete('file_secretariat_' + str(project_id))
        cache.delete('file_shop_' + str(project_id))
        cache.delete('projet_active')
        cache.delete('projet_active_calendar')
        cache.delete('projet_secretariat_active')
        cache.delete('projet_client_board')
        cache.delete('projet_secretariat_client_board')
        return Response("Deleted Successfully!!")
    

class ProjectCommentsPostView(APIView):
    #permission_classes = [IsAuthenticated,]
    def post(self, request, project_id):
        comment_data = JSONParser().parse(request)
        comment_serializer = CommentsToProjectPostSerializer(data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            cache.delete('file_project_'+ str(project_id))
            cache.delete('file_project_admin_' + str(project_id))
            cache.delete('file_secretariat_' + str(project_id))
            cache.delete('file_shop_' + str(project_id))
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response("Added Successfully!!")         
        return Response("Failed to Add")


class ComentProjectDeleteView(APIView):
    def delete(self, request, id=0, project_id=0):
        comment = CommentsToProject.objects.get(Comment_id=id)        
        comment.delete()
        cache.delete('file_project_'+ str(project_id))
        cache.delete('file_project_admin_' + str(project_id))
        cache.delete('file_secretariat_' + str(project_id))
        cache.delete('file_shop_' + str(project_id))
        cache.delete('projet_active')
        cache.delete('projet_active_calendar')
        cache.delete('projet_secretariat_active')
        cache.delete('projet_client_board')
        cache.delete('projet_secretariat_client_board')
        return Response("Deleted Successfully!!")