from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('user_create/',UserCreateView.as_view(),name='user-create'),

]