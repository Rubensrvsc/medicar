from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('user_create/',UserCreateView.as_view(),name='user-create'),
    path('obter_token/',ObterTokenView.as_view(),name='obter-token'),
    path('especialidades/',EspecialidadeListView.as_view(),name='especialidade-list'),
]