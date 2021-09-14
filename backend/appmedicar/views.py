from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now,localtime,localdate 
from django.db.models import Q
from .serializers import *
from .helpers.helper_agendas_livres import *
from .helpers.helper_desmarca_consulta import *
import pdb
# Create your views here.

class EspecialidadeListView(generics.ListAPIView):

    serializer_class = EspecialidadeSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        especialidade = Especialidade.objects.all()
        if search is not None:
            return especialidade.filter(nome_especialidade__icontains=search)
        return especialidade

class MedicoListView(generics.ListAPIView):

    serializer_class = MedicoListSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        especialidade = self.request.query_params.getlist('especialidade',None)
        medico = Medico.objects.all()

        if search:
            medico = medico.filter(nome_medico__icontains=search)
        elif especialidade:
            medico = medico.filter(especialidade_medico__id__in=list(especialidade))
        
        return medico

class ConsultaListView(generics.ListAPIView):

    serializer_class = ConsultaSerializerList

    def get_queryset(self):
        queryset = Consulta.objects.filter(cliente__username=self.request.user.username)
        queryset = queryset.exclude(Q(agenda__dia__lt=localdate()) | 
        Q(agenda__dia=localdate()) & 
        Q(horario__hora__lt=localtime())).order_by('agenda__dia'
        ).order_by('horario__hora')

        return queryset

class AgendaListView(generics.ListAPIView):

    serializer_class = AgendaSerializer
    queryset = Agenda.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        medico_params = self.request.query_params.getlist('medico',None)
        especialidade_params = self.request.query_params.getlist('especialidade',None)
        data_inicio = self.request.query_params.get('data_inicio',None)
        data_fim = self.request.query_params.get('data_fim',None)


        return agendas_filtro(medico_params,especialidade_params,data_inicio,data_fim,agendas_livres())


#Refatorar o Post desse método
class ConsultaCreateView(generics.CreateAPIView):

    serializer_class = ConsultaSerializerCreate
    permission_classes = [permissions.AllowAny]

#Refatorar o Destroy desse método
class DesmarcarConsultaView(generics.DestroyAPIView):
    serializer_class = DesmarcarConsultaSerializer
    queryset = Consulta.objects.all()

    def destroy(self, request,id):
        return desmarcar_consulta(id,self.request.user.username)


class UserCreateView(APIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        user = User(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
        user.save()
        usuario = User.objects.get(pk=user.pk)
        Token.objects.create(user=usuario)
        token = Token.objects.get(user=usuario)
        return Response({'token':token.key})

class ObterTokenView(APIView):

    serializer_class = ObterTokenSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Token.objects.all()

    def post(self,request):
        token = Token.objects.filter(Q(user__username = request.POST['username']) & 
        Q(user__password=request.POST['password'])).first()
        if token:
            return Response({'token':token.key})
        return Response(status=status.HTTP_404_NOT_FOUND)
