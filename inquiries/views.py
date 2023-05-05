from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
import shutil
import os

from .models import Inquiry
from .serializers import (
    InquiryPostSerializer, InquiryGetTableSerializer,
    InquiryGetDetailSerializer, InquiryPutSerializer
)


class InquiryPostView(APIView):
    #permission_classes = [IsAuthenticated,]
    def post(self, request):
        inquiry_data = JSONParser().parse(request)
        inquiry_serializer = InquiryPostSerializer(data=inquiry_data)
        if inquiry_serializer.is_valid():
            inquiry_serializer.save()            
            return Response("Added Successfully!!")
        return Response("Failed to Add")


class InquiryPutView(APIView):
    def put(self, request):
        inquiry_data = JSONParser().parse(request)
        inquiry = Inquiry.objects.get(Inquiry_id=inquiry_data['Inquiry_id'])
        inquiry_serializer = InquiryPutSerializer(inquiry, data=inquiry_data)
        if inquiry_serializer.is_valid():
            inquiry_serializer.save()
            return Response("Updated Successfully!!")        
        return Response("Failed to Update")
    

class InquiryGetNewView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        inquiries = Inquiry.objects.filter(
           Q(Inquiry_status="new")).order_by('-Inquiry_date_created')
        inquiries_serializer = InquiryGetTableSerializer(inquiries, many=True)
        return Response(inquiries_serializer.data)


class InquiryGetNewQuantityView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        inquiries_quantity = Inquiry.objects.filter(
           Q(Inquiry_status="new")).count()
        return Response(inquiries_quantity)
    

class InquiryAcceptedView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        inquiries = Inquiry.objects.filter(
           Q(Inquiry_status="accepted")).order_by('-Inquiry_date_created')
        inquiries_serializer = InquiryGetTableSerializer(inquiries, many=True)
        return Response(inquiries_serializer.data)
    

class InquiryRejectedView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        inquiries = Inquiry.objects.filter(
           Q(Inquiry_status="rejected")).order_by('-Inquiry_date_created')
        inquiries_serializer = InquiryGetTableSerializer(inquiries, many=True)
        return Response(inquiries_serializer.data)


class InquiryConsiderationView(APIView):
    #permission_classes = [IsAuthenticated,]

    def get(self, request):
        inquiries = Inquiry.objects.filter(
           Q(Inquiry_status="under_consideration")).order_by('-Inquiry_date_created')
        inquiries_serializer = InquiryGetTableSerializer(inquiries, many=True)
        return Response(inquiries_serializer.data)
    

class InquiryDeleteView(APIView):
    def delete(self, request, id=0):
        inquiry = Inquiry.objects.get(Inquiry_id=id)
        if os.path.isdir('assets/projects/Inquiry_' + str(id) + '/'):
            shutil.rmtree('assets/projects/Inquiry_' + str(id) + '/')
            inquiry.delete()
        inquiry.delete()
        return Response("Deleted Successfully!!")


class InquiryDetialView(generics.RetrieveAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquiryGetDetailSerializer