from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},            
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserToProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
            'role': {'required': False},
            'phone_number': {'required': False},
            'department': {'required': False},
            'address': {'required': False},            
            'own_description': {'required': False},
            'boss_description': {'required': False},
            'education': {'required': False},
            'experience': {'required': False},
        }


class ChangeAdminPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','new_password')
    
    def update(self, instance, validated_data):        
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    

class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password_1 = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','old_password', 'new_password_1', 'new_password_2')
    
    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({"error": "Old password is incorrect"})
        if validated_data['new_password_1'] != validated_data['new_password_2']:
            raise serializers.ValidationError({"error": "New Passwords are incorrect!!!"})
        instance.set_password(validated_data['new_password_1'])
        instance.save()
        return instance