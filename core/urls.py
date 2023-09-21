from django.urls import path
from .views import APIListUsersView, Login



urlpatterns = [
    path('api/login/', Login.as_view(), name='login' ),
    path('api/users/', APIListUsersView.as_view(), name='users-list'),
    
]
