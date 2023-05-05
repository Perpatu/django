from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
import os
from django.core.cache import cache

from django.http import FileResponse
from django.shortcuts import get_object_or_404

from projects.models import Project
from projects.serializers import ProjectPutSerializer
from .models import Files, FilesInquiry
from .serializers import (
    FilePutSerializer, FilesGetProjectSerializer,
    FilesGetSerializer, FilesUploadSerializer,
    FilesGetProjectAdminSerializer, FilesGetDepartmentsSerializer,
    FilesGetNumberDepartmentsSerializer, FilesUploadInquirySerializer,
    FilesGetInquirySerializer
)


class FileUploadView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, project_id):
        serializer = FilesUploadSerializer(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            message = {'detail': qs, 'status': True}
            cache.delete('file_project_'+ str(project_id))
            cache.delete('file_project_admin_' + str(project_id))
            cache.delete('file_secretariat_' + str(project_id))
            cache.delete('file_shop_' + str(project_id))
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response(message, status=status.HTTP_201_CREATED)
        data = {"detail": serializer.errors, 'status': False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class FileUploadInquiryView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = FilesUploadInquirySerializer(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            message = {'detail': qs, 'status': True}
            return Response(message, status=status.HTTP_201_CREATED)
        data = {"detail": serializer.errors, 'status': False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class FileDetialView(generics.RetrieveAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesGetSerializer


class FilesPutView(APIView):
    def put(self, request, project_id):
        file_data = JSONParser().parse(request)
        file = Files.objects.get(File_id=file_data['File_id'])
        file_serializer = FilePutSerializer(file, data=file_data)
        if file_serializer.is_valid():
            file_serializer.save()
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


class DownloadView(generics.RetrieveAPIView):
    def get(self, request, id):
        my_model = get_object_or_404(Files, File_id=id)
        files = my_model.file
        return FileResponse(files)


class FilesDeleteView(APIView):
    def delete(self, request, id=0, project_id=0):
        file = Files.objects.get(File_id=id)
        path_file = str(file.file)
        os.remove('assets/projects/' + path_file)
        file.delete()
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


class FileProjectGetView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, project_id):
        cache_key = 'file_project_' + str(project_id)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        files = Files.objects.filter(
            Q(Project_id=project_id) & Q(File_destiny='Production')).order_by('filename')
        files_serializer = FilesGetProjectSerializer(files, many=True)
        key_list = []
        file_choose = []
        file_end = []
        for key in files_serializer.data:
            key_list = list(key.keys())
            break
        for cos in files_serializer.data:
            for keys in key_list:
                if keys != 'file' and keys != 'filename' and keys != 'comments':
                    if type(cos[keys]) != str:
                        if cos[keys]['chosen']:
                            file_choose.append(cos[keys]['chosen'])
                    if not isinstance(cos[keys]['Queue_logic'], str):
                        if cos[keys]['Queue_logic']['User_end']:
                            file_end.append(
                                cos[keys]['Queue_logic']['User_end'])
        project_progress = 0
        if len(file_end) != 0 and len(file_choose) != 0:
            project_progress = (len(file_end) / len(file_choose)) * 100

        if project_progress == 100.0:
            project_update = {'Project_id': project_id,
                              'Project_progress': round(project_progress),
                              'Project_status': 'Completed'}
        else:
            project_update = {'Project_id': project_id,
                              'Project_progress': round(project_progress),
                              'Project_status': 'Started'}
        project = Project.objects.filter(Project_id=project_id).first()
        project_serializer = ProjectPutSerializer(project, data=project_update)
        if project_serializer.is_valid():
            project_serializer.save()

        data = files_serializer.data

        cache.set(cache_key, data, timeout=10000)
        return Response(data)


class FileProjectAdminGetView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, project_id):
        cache_key = 'file_project_admin_' + str(project_id)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        files = Files.objects.filter(
            Q(Project_id=project_id) & Q(File_destiny='Production')).order_by('filename')
        files_serializer = FilesGetProjectAdminSerializer(files, many=True)
        data = files_serializer.data

        cache.set(cache_key, data, timeout=10000)
        return Response(data)


class FileSecretariatGetView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, project_id):
        cache_key = 'file_secretariat_' + str(project_id)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        files = Files.objects.filter(
            Q(Project_id=project_id) & Q(File_destiny='Secretariat')).order_by('File_id')
        files_serializer = FilesGetSerializer(files, many=True)
        data = files_serializer.data

        cache.set(cache_key, data, timeout=10000)
        return Response(data)


class FileShopGetView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request, project_id):
        cache_key = 'file_shop_' + str(project_id)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        files = Files.objects.filter(Q(Project_id=project_id) & Q(
            File_destiny='Shop')).order_by('File_id')
        files_serializer = FilesGetSerializer(files, many=True)

        data = files_serializer.data

        cache.set(cache_key, data, timeout=10000)
        return Response(data)


class FilesDepartmentsGetView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, dep):        
        files = Files.objects.filter(
            Q(File_destiny='Production') & Q(Queue__Departments_name=dep)).order_by('File_id')
        files_serializer = FilesGetDepartmentsSerializer(
            files, many=True, context={'dep': dep.lower()})           
        return Response(files_serializer.data)


class FilesNumberDepartment(APIView):
    # permission_classes = [IsAuthenticated,]
    def get(self, request, dep):
        
        dep_low = dep.lower()
        files_quantity = Files.objects.filter(
            Q(File_destiny='Production') & Q(Queue__Departments_name=dep)).count()
        files_query = Files.objects.filter(
            Q(File_destiny='Production') & Q(Queue__Departments_name=dep)).order_by('File_id')
        files_serializer = FilesGetNumberDepartmentsSerializer(
            files_query, many=True, context={'dep': dep_low, 'quantity': files_quantity})
        response = {}
        if len(files_serializer.data) > 0:
            for key in files_serializer.data:
                dep = list(key.keys())[0]
                response[dep] = {'Department_name': dep,
                                 'quantity': files_quantity}
                break
        else:
            response[dep_low] = {'Department_name': dep, 'quantity': 0}

        return Response(response)


class FilesInquiryGetView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, id):
        files = FilesInquiry.objects.filter(
            Q(Inquiry=id)).order_by('File_id')
        files_serializer = FilesGetInquirySerializer(files, many=True)
        return Response(files_serializer.data)


class FilesInquiryDeleteView(APIView):
    def delete(self, request, id=0):
        file = FilesInquiry.objects.get(File_id=id)
        path_file = str(file.file)
        os.remove('assets/projects/' + path_file)
        file.delete()
        return Response("Deleted Successfully!!")
    

class DownloadInquiryView(generics.RetrieveAPIView):
    def get(self, request, id):
        my_model = get_object_or_404(FilesInquiry, File_id=id)
        files = my_model.file
        return FileResponse(files)