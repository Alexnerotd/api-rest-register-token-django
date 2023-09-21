from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .serializers import MyUser, MyUserSerializerGET, MyUserSerializerPOST

from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

# Clase para enlistar(GET) a todos los usuarios regstrados en la API.

class APIListUsersView(APIView):

    def get(self, request, format = None):
        user = MyUser.objects.all()
        user_serializer = MyUserSerializerGET(user, many = True)
        try:
            if user_serializer:
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'message': 'No existen usuario registrados hasta el momento'}, status=status.HTTP_404_NOT_FOUND)
        

''' Clase para Agregar(POST) a usuarios a la API,
    encryptando la contrasena y generando un Token personal,
    heredando de ObtainAuthToken
'''
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context = {"request":request})
        if login_serializer.is_valid():
            print("La validacion paso con exito")
        return Response({'message':"Hola desde response"}, status=status.HTTP_200_OK)
