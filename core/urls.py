from django.urls import path
from .views import APIListUsersView



urlpatterns = [
    path('api/users/', APIListUsersView.as_view(), name='users-list'),
    
]
