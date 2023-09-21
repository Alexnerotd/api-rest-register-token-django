from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.sessions.models import Session


from .serializers import MyUser, MyUserSerializerGET, MyUserSerializerPOST

from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from datetime import datetime
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
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = MyUserSerializerGET(user)
                if created:
                    return Response({'token': token.key,
                                     'user': user_serializer.data,
                                     'message': 'Inicio de sesion exitoso.'}, status=status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({'token': token.key,
                                     'user': user_serializer.data,
                                     'message': 'Inicio de sesion exitoso.'}, status=status.HTTP_201_CREATED)
                

            else:
                return Response({'error':"Este usuario no puede iniciar sesion"}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response({'error': 'Los datos ingresados son incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':"Hola desde response"}, status=status.HTTP_200_OK)
