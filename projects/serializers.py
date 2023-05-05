from rest_framework import serializers
from .models import Project
from users.models import User
from users.serializers import UserToProjectSerializer
from comments.serializers import CommentsToProjectGetSerializer
from comments.models import CommentsToProject
from clients.serializers import ClientGetSerializer



class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

        extra_kwargs = {
            'Project_name': {'required': False},
            'Project_group': {'required': False},
            'User': {'required': False},
            'Client': {'required': False},
            'Project_end_date': {'required': False},
            'Project_date_created': {'required': False},
            'Project_progress': {'required': False},
            'Project_priority': {'required': False},
            'Project_status': {'required': False},
            'Project_number': {'required': False},
            'Project_or_order': {'required': False},
            'Project_order_number': {'required': False},
            'Project_message': {'required': False},
            'Project_secretariat': {'required': False},
            'Project_invoice': {'required': False},
        }


class ProjectGetSerializer(serializers.ModelSerializer):

    Files_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='File_id'
    )

    Comments_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='Comment_id'
    )

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['User'] = UserToProjectSerializer(instance.User).data
        return response


class ProjectGetDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='Project_id'
    )

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['User'] = {'id': UserToProjectSerializer(instance.User).data['id'],
                            'first_name': UserToProjectSerializer(instance.User).data['first_name'],
                            'last_name': UserToProjectSerializer(instance.User).data['last_name']}
        response['Client'] = {'id': ClientGetSerializer(instance.Client).data['Client_id'],
                              'Client_name': ClientGetSerializer(instance.Client).data['Client_name']
                              }
        com_data = []
        for i, com in enumerate(response['comments']):            
            comments = CommentsToProject.objects.filter(Project=com)
            comments_serializer = CommentsToProjectGetSerializer(comments, many=True)
            com_data.append({
                        'id': comments_serializer.data[i]['Comment_id'],
                        'text': comments_serializer.data[i]['Text'],
                        'user': comments_serializer.data[i]['User']['first_name'] + ' ' + comments_serializer.data[i]['User']['last_name'],
                        })
        response['comments'] = com_data
        return response


class ProjectGetBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['Project_group_to_update'] = response['Project_group']
        response['User'] = {'id': UserToProjectSerializer(instance.User).data['id'],
                            'first_name': UserToProjectSerializer(instance.User).data['first_name'],
                            'last_name': UserToProjectSerializer(instance.User).data['last_name']}
        
        response['Client'] = {'id': ClientGetSerializer(instance.Client).data['Client_id'],
                              'Client_name': ClientGetSerializer(instance.Client).data['Client_name'],
                              'Color': ClientGetSerializer(instance.Client).data['Color']}
        
        if len(response['Project_group']) > 0:

            users = []
            for id in response['Project_group']:
                user = User.objects.filter(id=id)
                user_serializer = UserToProjectSerializer(user, many=True)
                users.append(user_serializer.data[0])
                
            response['Project_group'] = users

        return response


class ProjectActiveClientBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['User'] = {'id': UserToProjectSerializer(instance.User).data['id'],
                            'first_name': UserToProjectSerializer(instance.User).data['first_name'],
                            'last_name': UserToProjectSerializer(instance.User).data['last_name']}
        
        response['Client'] = {'id': ClientGetSerializer(instance.Client).data['Client_id'],
                              'Client_name': ClientGetSerializer(instance.Client).data['Client_name'],
                              'Color': ClientGetSerializer(instance.Client).data['Color']}       

        return response