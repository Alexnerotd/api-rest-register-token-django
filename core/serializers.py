from rest_framework import serializers
from .models import MyUser

class MyUserSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'name', 'last_name']


class MyUserSerializerPOST(serializers.ModelSerializer):

    class Meta: 
        model = MyUser
        fields = ['username', 'email', 'password', 'name', 'last_name']


    def create(self, validate_data):
        user = MyUser(**validate_data)
        user.set_password(validate_data['password'])
        user.save()
        return user