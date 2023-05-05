from rest_framework import serializers
from .models import CommentsToFile, CommentsToProject
from users.serializers import UserSerializer


class CommentsToFilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsToFile
        fields = "__all__"


class CommentsToFileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsToFile
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['User'] = {'id': UserSerializer(instance.User).data['id'],
                            'first_name': UserSerializer(instance.User).data['first_name'],
                            'last_name': UserSerializer(instance.User).data['last_name']}
        del response['File']
        return response

class CommentsToProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsToProject
        fields = '__all__'


class CommentsToProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsToProject
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['User'] = {'id': UserSerializer(instance.User).data['id'],
                            'first_name': UserSerializer(instance.User).data['first_name'],
                            'last_name': UserSerializer(instance.User).data['last_name']}
        return response


