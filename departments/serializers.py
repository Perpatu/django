from rest_framework import serializers
from .models import Departments


class DepartmentsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('Departments_id', 'Departments_name','Departments_order')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)             
        return response


class DepartmentsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'


class DepartmentsPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
    
    extra_kwargs = {
        'Departments_name': {'required': False},
        'Static': {'required': False},
    }


class AdminColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('Departments_name',)


