from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyManager(BaseUserManager):

    def create_user(self, email, username, password = None):

        if not email:
            raise ValueError('The user need a email value')
        user = self.model(
            email = self.normalize_email(email=email),
            username = username,
        )

        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email,
            username = username,
            password = password,
        )

        user.is_admin = True
        user.save()
        return user
    


