from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import Client
from .serializers import ClientGetSerializer, ClientPostSerializer



class ClientGetView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        cache_key = 'client'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
    
        client = Client.objects.all().order_by('Client_name')
        client_serializer = ClientGetSerializer(client, many=True)
        data = client_serializer.data

        cache.set(cache_key, data, timeout=10000)

        return Response(data)


class ClientPostView(APIView):
    def post(self, request):
        client_data = JSONParser().parse(request)
        client_serializer = ClientPostSerializer(data=client_data)
        if client_serializer.is_valid():
            client_serializer.save()
            cache.delete('client')
            return Response("Added Successfully!!")        
        return Response("Failed to Add")


class ClientPutView(APIView):
    def put(self, request):
        client_data = JSONParser().parse(request)
        client = Client.objects.get(Client_id=client_data['Client_id'])
        client_serializer = ClientPostSerializer(client, data=client_data)
        if client_serializer.is_valid():
            client_serializer.save()
            cache.delete('client')
            return Response("Updated Successfully!!")        
        return Response("Failed to Update")


class ClientDeleteView(APIView):
    def delete(self, request, id=0):
        client = Client.objects.get(Client_id=id)
        client.delete()
        cache.delete('client')
        return Response("Deleted Successfully!!")


class ClientDatailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientGetSerializer
    
    