from rest_framework import serializers
from users.serializers import UserToProjectSerializer
from .models import Inquiry


class InquiryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'


class InquiryPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        extra_kwargs = {
            'Project_name': {'required': False},
            'User': {'required': False},
            'Inquiry_date_created': {'required': False},
            'Client': {'required': False},
            'Inquiry_name': {'required': False},
            'Inquiry_content': {'required': False},
            'Comapny_name': {'required': False},
            'Inquiry_status': {'required': False},
        }

class InquiryGetTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['User'] is not None:
            response['User'] = {'id': UserToProjectSerializer(instance.User).data['id'],
                                'first_name': UserToProjectSerializer(instance.User).data['first_name'],
                                'last_name': UserToProjectSerializer(instance.User).data['last_name']}
        return response


class InquiryGetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
    

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['User'] is not None:
            response['User'] = {'id': UserToProjectSerializer(instance.User).data['id'],
                                'first_name': UserToProjectSerializer(instance.User).data['first_name'],
                                'last_name': UserToProjectSerializer(instance.User).data['last_name']}
        return response