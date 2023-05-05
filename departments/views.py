from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics, status
from django.db.models import Q

from files.models import Files 
from .models import Departments
from .serializers import (
    DepartmentsGetSerializer, DepartmentsPutSerializer,
    DepartmentsPostSerializer, AdminColumnSerializer, 
)


class DepartmentsToColumnView(APIView):
    #permission_classes = [IsAuthenticated,]
    def get(self, request):  

              
        departments = Departments.objects.all().order_by('Departments_order')        
        departments_serializer = DepartmentsGetSerializer(departments, many=True)    
        departments_list = []        
        response = {}
        for dep in departments_serializer.data:            
            departments_list.append(dep['Departments_name'])
        departments_list.insert(0, 'filename')
        departments_list.insert(0, 'File')
        departments_list.insert(0, 'Delete')
        departments_list.append('Comments')
        response['Departments_name'] = departments_list
        return Response(response)


class DepartmentsGetAllView(APIView):
    #permission_classes = [IsAuthenticated,]
    def get(self, request):
        
        departments = Departments.objects.all().order_by('Departments_order')              
        departments_serializer = DepartmentsGetSerializer(departments, many=True)
        return Response(departments_serializer.data)


class DepartmentsGetMainView(APIView):
    #permission_classes = [IsAuthenticated,]
    def get(self, request): 
        
        departments = Departments.objects.all().order_by('Departments_order')              
        departments_serializer = DepartmentsGetSerializer(departments, many=True)

        for dep in departments_serializer.data:
            files_quantity = Files.objects.filter(
                Q(File_destiny='Production') & Q(Queue__Departments_name=dep['Departments_name'])).count()            
            dep['quantity'] = files_quantity

        return Response(departments_serializer.data)
        

class AdminCloumnGetView(APIView):
    #permission_classes = [IsAuthenticated,]
    def get(self, request):             
        
        departments = Departments.objects.all().order_by('Departments_order')              
        departments_serializer = AdminColumnSerializer(departments, many=True)      
        column_name = ['Delete', 'File', 'filename'] 
        response = {}
        for dep in departments_serializer.data:            
            column_name.append(dep['Departments_name'])          
        response['Departments_name'] = column_name
        return Response(response)


class DepartmentCloumnGetView(APIView):
    #permission_classes = [IsAuthenticated,]
    def get(self, request, dep):        
        
        column_name = ['File', 'filename', dep.lower(), 'Comments'] 
        response = {}          
        response['Departments_name'] = column_name  

        return Response(response)


class DepartmentsPostView(APIView):
    def post(self, request):        
        departments_data = JSONParser().parse(request)
        departments_serializer = DepartmentsPostSerializer(
            data=departments_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return Response("Added Successfully!!", status=status.HTTP_200_OK)
        return Response(departments_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DepartmentsPutView(APIView):
    def put(self, request):
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(Departments_id=department_data['Departments_id'])
        department_serializer = DepartmentsPutSerializer(department, data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return Response("Updated Successfully!!")          
        return Response("Failed to Update")


class DepartmentsDeleteView(APIView):
    def delete(self, request, id=0):
        department = Departments.objects.get(Departments_id=id)
        department.delete()
        return Response("Deleted Successfully!!")


class DepartmentDetialView(generics.RetrieveAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsGetSerializer


