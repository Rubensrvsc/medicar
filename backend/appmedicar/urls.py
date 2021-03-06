from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('user_create/',UserCreateView.as_view(),name='user-create'),
    path('obter_token/',ObterTokenView.as_view(),name='obter-token'),
    path('especialidades/',EspecialidadeListView.as_view(),name='especialidade-list'),
    path('medicos/',MedicoListView.as_view(),name='medico-list'),
    path('consultas/',ConsultaListView.as_view(),name='consultas-list'),
    path('agendar_consulta/',ConsultaCreateView.as_view(),name='create-consulta'),
    path('agendas/',AgendaListView.as_view(),name='agendas-list'),
    path('desmarcar_consulta/<int:id>',DesmarcarConsultaView.as_view(),name='desmarcar-consulta'),
]