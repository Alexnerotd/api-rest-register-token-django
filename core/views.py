from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .serializers import MyUser, MyUserSerializerGET, MyUserSerializerPOST

from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response

# Create your views here.
class APIListUsersView(APIView):

    def get(self, request, format = None):
        user = MyUser.objects.all()
        user_serializer = MyUserSerializerGET(user, many = True)
        try:
            if user_serializer:
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'message': 'No existen usuario registrados hasta el momento'}, status=status.HTTP_404_NOT_FOUND)
        