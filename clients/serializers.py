from rest_framework import serializers
from .models import Client


class ClientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        depth = 1