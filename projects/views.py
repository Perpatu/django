from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from django.core.cache import cache
import shutil
import os

from .models import Project
from .serializers import (
    ProjectGetBoardSerializer, ProjectGetDetailSerializer,
    ProjectPostSerializer, ProjectPutSerializer,
    ProjectActiveClientBoardSerializer
)


class ProjectPostView(APIView):
    # permission_classes = [IsAuthenticated,]
    def post(self, request):
        project_data = JSONParser().parse(request)
        project_serializer = ProjectPostSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_completed')
            cache.delete('projet_paused')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_secretariat_completed')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response("Added Successfully!!")
        return Response("Failed to Add")


class ProjectPutView(APIView):
    def put(self, request):
        project_data = JSONParser().parse(request)
        project = Project.objects.get(Project_id=project_data['Project_id'])
        project_serializer = ProjectPutSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_completed')
            cache.delete('projet_paused')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_secretariat_completed')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
            return Response("Updated Successfully!!")
        return Response("Failed to Update")


class ProjectDeleteView(APIView):
    def delete(self, request, id=0):
        project = Project.objects.get(Project_id=id)
        if os.path.isdir('assets/projects/' + str(id) + '/'):
            shutil.rmtree('assets/projects/' + str(id) + '/')
            project.delete()
            cache.delete('projet_active')
            cache.delete('projet_active_calendar')
            cache.delete('projet_completed')
            cache.delete('projet_paused')
            cache.delete('projet_secretariat_active')
            cache.delete('projet_secretariat_completed')
            cache.delete('projet_client_board')
            cache.delete('projet_secretariat_client_board')
        project.delete()
        return Response("Deleted Successfully!!")


class ProjectDetialView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectGetDetailSerializer


class ProjectActiveView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_active'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(
            Q(Project_status="In design") | Q(Project_status="Started")).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        data = projects_serializer.data

        cache.set(cache_key, data, timeout=10000)

        return Response(data)


class ProjectActiveCalendarView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_active_calendar'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(
            Q(Project_status="In design") | Q(Project_status="Started") & ~Q(Project_id=237)).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        data = projects_serializer.data

        cache.set(cache_key, data, timeout=10000)

        return Response(data)


class ProjectCompletedView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_completed'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(
            Project_status="Completed").order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        data = projects_serializer.data

        cache.set(cache_key, data, timeout=216000)
        return Response(projects_serializer.data)


class ProjectPausedView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_paused'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(
            Project_status="Suspended").order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)

        data = projects_serializer.data

        cache.set(cache_key, data, timeout=216000)
        return Response(data)


class ProjectUserActiveView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, User_id):
        projects = Project.objects.filter(
            Q(User_id=User_id) & Q(Project_status="Started") | Q(Project_status="In design")).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        return Response(projects_serializer.data)


class ProjectUserCompletedView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, User_id):
        projects = Project.objects.filter(
            Q(User_id=User_id) & Q(Project_status="Completed")).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        return Response(projects_serializer.data)


class ProjectSecretariatActiveView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_secretariat_active'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(
            Q(Project_secretariat=True) & Q(Project_invoice="NO")).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        data = projects_serializer.data

        cache.set(cache_key, data, timeout=10000)

        return Response(data)


class ProjectSecretariatCompletedView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_secretariat_completed'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        projects = Project.objects.filter(Q(Project_secretariat=True) & Q(
            Project_invoice="YES") | Q(Project_invoice="YES (LACK OF INVOICE)")).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        data = projects_serializer.data

        cache.set(cache_key, data, timeout=10000)
        return Response(data)


class ProjectActiveClientView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request, client):
        projects = Project.objects.filter(
            (Q(Project_status="In design") | Q(Project_status="Started")) &
            Q(Client__Client_name=client)).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        return Response(projects_serializer.data)


class ProjectCompletedClientView(APIView):
    # permission_classes = [IsAuthenticated,]
    def get(self, request, client):
        projects = Project.objects.filter(
            Q(Project_status="Completed") &
            Q(Client__Client_name=client)).order_by('-Project_date_created')
        projects_serializer = ProjectGetBoardSerializer(projects, many=True)
        return Response(projects_serializer.data)


class ProjectActiveClientBoardView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_client_board'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        projects = Project.objects.filter(
            (Q(Project_status="In design") | Q(Project_status="Started"))).order_by('-Project_date_created')
        projects_serializer = ProjectActiveClientBoardSerializer(
            projects, many=True)
        client_projects = {}
        client_projects_list = []
        for client in projects_serializer.data:
            client_projects_query = Project.objects.filter(
                (Q(Project_status="In design") | Q(Project_status="Started")) &
                Q(Client__Client_name=client['Client']['Client_name'])).order_by('-Project_date_created')
            client_projects_serializer = ProjectGetBoardSerializer(
                client_projects_query, many=True)
            if client['Client']['Client_name'] == client_projects_serializer.data[0]['Client']['Client_name']:
                client_projects[client['Client']['Client_name']
                                ] = client_projects_serializer.data
        for client in client_projects:
            client_projects_list.append({client: client_projects[client]})
        
        data = client_projects_list

        cache.set(cache_key, data, timeout=10000)

        return Response(data)


class ProjectActiveClientBoardSecretariatView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'projet_secretariat_client_board'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        projects = Project.objects.filter(
            (Q(Project_status="In design") | Q(Project_status="Started") | (Q(Project_secretariat=True) & Q(Project_invoice="NO")))).order_by('-Project_date_created')
        projects_serializer = ProjectActiveClientBoardSerializer(
            projects, many=True)
        client_projects = {}
        client_projects_list = []
        for client in projects_serializer.data:
            client_projects_query = Project.objects.filter(
                (Q(Project_status="In design") | Q(Project_status="Started") | (Q(Project_secretariat=True) & Q(Project_invoice="NO"))) &
                Q(Client__Client_name=client['Client']['Client_name'])).order_by('-Project_date_created')
            client_projects_serializer = ProjectGetBoardSerializer(
                client_projects_query, many=True)
            if client['Client']['Client_name'] == client_projects_serializer.data[0]['Client']['Client_name']:
                client_projects[client['Client']['Client_name']] = client_projects_serializer.data
        for client in client_projects:
            client_projects_list.append({client: client_projects[client]})
        
        data = client_projects_list

        cache.set(cache_key, data, timeout=10000)

        return Response(data)
