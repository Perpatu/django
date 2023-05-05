from rest_framework import serializers
from .models import Files, FilesInquiry
from .validators import validate_file_extension, validate_file_inquiry_extension
from queueFile.models import FileQueue
from departments.models import Departments
from comments.models import CommentsToFile
from departments.serializers import DepartmentsGetSerializer, AdminColumnSerializer
from queueFile.serializers import QueueGetSerializer, QueueGetIdSerializer
from comments.serializers import CommentsToFileGetSerializer
from django.db.models import Q


class FilesUploadSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False
        ))

    class Meta:
        model = Files
        fields = '__all__'

    def create(self, validated_data):
        Project = validated_data['Project']
        User = validated_data['User']
        File_destiny = validated_data['File_destiny']
        file = validated_data.pop('file')
        file_list = []

        for file in file:
            file_name_str = str(file).lower()
            file_split = file_name_str.split('.')
            file_extension = file_split[-1]
            if validate_file_extension(file_extension):
                file_obj = Files.objects.create(
                    file=file, Project=Project, User=User, File_destiny=File_destiny, filename=file.name)
                fileurl = f'{file_obj.file.url}'
                file_list.append(fileurl)
            else:
                raise serializers.ValidationError('Wrong file format')
        return file_list


class FilesUploadInquirySerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False
        ))

    class Meta:
        model = FilesInquiry
        fields = '__all__'

    def create(self, validated_data):
        Inquiry = validated_data['Inquiry']       
        file = validated_data.pop('file')
        file_list = []

        for file in file:
            file_name_str = str(file).lower()
            file_split = file_name_str.split('.')
            file_extension = file_split[-1]
            if validate_file_inquiry_extension(file_extension):
                file_obj = FilesInquiry.objects.create(
                    file=file, Inquiry=Inquiry, filename=file.name)
                fileurl = f'{file_obj.file.url}'
                file_list.append(fileurl)
            else:
                raise serializers.ValidationError('Wrong file format')
        return file_list


class FilesGetSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='File_id'
    )
    class Meta:
        model = Files
        fields = ('File_id', 'file', 'filename', 'Queue', 'comments')
        extra_kwargs = {
            'File_destiny': {'required': False},
            'file': {'required': False},
            'User_upload': {'required': False},
            'Project': {'required': False},
            'filename': {'required': False},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)   

        com_data = []        
        for i, com in enumerate(response['comments']):      
            comments = CommentsToFile.objects.filter(File=com)
            comments_serializer = CommentsToFileGetSerializer(comments, many=True)           
            com_data.append({
                        'id': comments_serializer.data[i]['Comment_id'],
                        'text': comments_serializer.data[i]['Text'],
                        'user': comments_serializer.data[i]['User']['first_name'] + ' ' + comments_serializer.data[i]['User']['last_name'],
                        })
       
        response['comments'] = {'comments':com_data,
                                'File_id':response['File_id']}
        return response


class FilesGetProjectAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = ('File_id', 'file', 'filename', 'Project',
                  'Queue')
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)        
        departments = Departments.objects.all()

        response['delete'] = {           
            'File_id': response['File_id']
        }

        response['file'] = {
            'filename': response['filename'],
            'File_id': response['File_id']
        }
        response['filename'] = {           
            'filename': response['filename'],
            'File_id': response['File_id']
        }               

        for dep in departments:
            dep_name = dep.Departments_name.lower()            
            response[dep_name] = {
                'Department_id': dep.Departments_id,
                'Department_name': dep_name,
                'Project': response['Project']['Project_id'],
                'File_id': response['File_id'],
                'Queue_choice': [q['Departments_id'] for q in response['Queue']],
                'order': dep.Departments_order
            }
            
            queue_logic = FileQueue.objects.filter(File=response['File_id'], Department=dep.Departments_id).order_by('Queue_id')
            if queue_logic.exists():                
                queue_serializer = QueueGetIdSerializer(queue_logic.first())
                response[dep_name]['chosen'] = True
                response[dep_name]['Queue_logic'] = queue_serializer.data['Queue_id']                
            else:
                response[dep_name]['chosen'] = False
                response[dep_name]['Queue_logic'] = ''      
        del response['Queue']
        del response['File_id']
        del response['Project']
        return response


class FilesGetProjectSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='File_id'
    )
    
    files_admin = FilesGetProjectAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Files
        fields = ('File_id', 'file', 'filename', 'files_admin', 'comments', 'Queue', 'Project')
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        departments = Departments.objects.all()
        com_data = []        
        for i, com in enumerate(response['comments']):                
            comments = CommentsToFile.objects.filter(File=com)
            comments_serializer = CommentsToFileGetSerializer(comments, many=True)           
            com_data.append({
                        'id': comments_serializer.data[i]['Comment_id'],
                        'text': comments_serializer.data[i]['Text'],
                        'user': comments_serializer.data[i]['User']['first_name'] + ' ' + comments_serializer.data[i]['User']['last_name'],
                        'Project_id': response['Project']['Project_id'],
                        })
       
        response['comments'] = {'comments':com_data,
                                'File_id':response['File_id']}  
        project_admin_instance = instance
        project_admin_serializer = FilesGetProjectAdminSerializer(project_admin_instance)
        response['files_admin'] = project_admin_serializer.to_representation(project_admin_instance)
        response['file'] = response['File_id']
        response['filename'] = {           
            'filename': response['filename'],
            'File_id': response['File_id']
        }
        
        for dep in departments:    
            
            dep_name = dep.Departments_name.lower()                 
            if dep_name in response['files_admin']:
                response[dep_name] = response['files_admin'][dep_name]
                response[dep_name]['Dep_choice_id'] = response[dep_name]['Queue_choice']
                response[dep_name]['Queue_choice'] = [q['Departments_order'] for q in response['Queue']]
                response[dep_name]['order'] = dep.Departments_order
                response[dep_name]['Departments_name'] = dep_name
            if response[dep_name]['Queue_logic'] != "":
                queue_logic = FileQueue.objects.filter(File=response[dep_name]['File_id'], Department=dep.Departments_id).order_by('Queue_id')
                queue_serializer = QueueGetSerializer(queue_logic.first())
                response[dep_name]['Queue_logic'] = queue_serializer.data
                response[dep_name]['permission'] = False              
                if len(response[dep_name]['Queue_choice']) > 0:          
                    if min(response[dep_name]['Queue_choice']) == dep.Departments_order:                 
                        response[dep_name]['order'] = dep.Departments_order      
                        response[dep_name]['permission'] = True
        del response['files_admin']
        del response['File_id']
        del response['Queue']
        del response['Project']
        return response


class FilesGetDepartmentsSerializer(serializers.ModelSerializer):

    files_project = FilesGetProjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Files
        fields = ( 'files_project', 'Project')
        depth=1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        dep = self.context.get('dep')
        files_project_instance = instance
        files_project_serializer = FilesGetProjectSerializer(files_project_instance)
        response['files_project'] = files_project_serializer.to_representation(files_project_instance)
        if response['files_project'][dep] != dep:
            response['file'] = response['files_project']['file']
            response['filename'] = response['files_project']['filename']
            #response['project'] = response['files_project']['File_id']            
            response['comments'] = response['files_project']['comments']
            response[dep] = response['files_project'][dep]       
            response['Projekt'] = response['Project']['Project_id']
        del response['files_project']
        del response['Project']              
        return response
    

class FilesGetNumberDepartmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Files
        fields = ('File_id',)
        depth=1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        dep = self.context.get('dep')
        files_number = self.context.get('quantity')
        response[dep] = files_number
        del response['File_id']
        return response
    

class FilePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

        extra_kwargs = {
            'File_destiny': {'required': False},
            'file': {'required': False},
            'User': {'required': False},
            'Project': {'required': False},
            'filename': {'required': False},
            'Queue': {'required': False},
        }


class FilesGetInquirySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FilesInquiry
        fields = '__all__'


    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response