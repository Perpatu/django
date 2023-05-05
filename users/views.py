from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics
import jwt

from .models import User
from .serializers import (
    UserSerializer, ChangeAdminPasswordSerializer,
    ChangeUserPasswordSerializer, UserUpdateSerializer
)


class RegisterView(APIView):
    #permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        user_data = JSONParser().parse(request)
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response("Added Successfully!!")
        print(serializer.errors)
        return Response("Failed to Add")       


class LoginView(APIView):
    # permission_classes = [AllowAny,]
    def post(self, request):
        name = request.data['name']
        password = request.data['password']
        user = User.objects.filter(username=name).first()
        if user is None:
            raise AuthenticationFailed('Wrong username')
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password')
        payload = {
            'id': user.id            
        }
        encoded_token = jwt.encode(payload, 'secret', algorithm='HS256')               
        response = Response()
        response.set_cookie(key='jwt', value=encoded_token, httponly=True)
        response.data = {
            'jwt': encoded_token
        }       
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class AdminChangePasswordView(APIView):
    #permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request):
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = ChangeAdminPasswordSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Updated Successfully!!")
        return Response("Failed to Update")


class UserChangePasswordView(APIView):
    #permission_classes = [IsAuthenticated,]

    def put(self, request):
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = ChangeUserPasswordSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Updated Successfully!!")
        return Response("Failed to Update")


class UserGetCurrentView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserChangeView(APIView):
    def put(self, request):
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = UserUpdateSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Updated Successfully!!")
        return Response("Failed to Update")
    

class UserDeleteView(APIView):
    def delete(self, request, id=0):
        user = User.objects.get(id=id)
        user.delete()
        return Response("Deleted Successfully!!")


class UsersGetAllView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.all().order_by("last_name")
        users_serializer = UserSerializer(user, many=True)
        return Response(users_serializer.data)


class UserNotAdminView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.filter(is_staff=False).order_by("last_name")
        users_serializer = UserSerializer(user, many=True)
        return Response(users_serializer.data)


class UserAdminView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.filter(is_staff=True).order_by("last_name")
        users_serializer = UserSerializer(user, many=True)
        return Response(users_serializer.data)


class UserDetailView(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()
    serializer_class = UserSerializer