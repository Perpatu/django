from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from django.core.cache import cache

from .serializers import QueueGetSerializer, QueuePostSerializer, QueuePutSerializer
from .models import FileQueue



class QueueFilePostView(APIView):
    #permission_classes = [IsAuthenticated,]

    def post(self, request, project_id):
        queue_data = JSONParser().parse(request)
        queue_serializer = QueuePostSerializer(data=queue_data)
        if queue_serializer.is_valid():
            queue_serializer.save()
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


class QueueFileGetView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        queue = FileQueue.objects.all()
        queue_serializer = QueueGetSerializer(queue, many=True)
        return Response(queue_serializer.data)


class QueueDeleteView(APIView):
    def delete(self, request, id=0, project_id=0):
        queue = FileQueue.objects.get(Queue_id=id)        
        queue.delete()
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


class FilesPutView(APIView):
    def put(self, request, project_id):
        queue_data = JSONParser().parse(request)
        file = FileQueue.objects.get(Queue_id=queue_data['Queue_id'])
        queue_serializer = QueuePutSerializer(file, data=queue_data)
        if queue_serializer.is_valid():
            queue_serializer.save()
            cache.delete('file_project_'+ str(project_id))
            cache.delete('file_project_admin_' + str(project_id))
            cache.delete('file_secretariat_' + str(project_id))
            cache.delete('file_shop_' + str(project_id))
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response("Updated Successfully!!")    
        return Response("Failed to Update")