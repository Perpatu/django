from rest_framework import serializers
from .models import FileQueue


class QueueGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileQueue
        fields = ('Queue_id', 'User_start', 'User_paused', 'User_end', 'Admin_allows', 'File')
   

class QueuePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileQueue
        fields = '__all__'
    

class QueuePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileQueue
        fields = '__all__'
        extra_kwargs = {
            'File': {'required': False},
            'Department': {'required': False},
        }


class QueueGetIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileQueue
        fields = ('Queue_id','Department')
        depth = 1
