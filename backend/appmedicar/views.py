from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now,localtime,localdate 
from django.db.models import Q
from .serializers import *
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
    permission_classes = [permissions.AllowAny]

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
        queryset = Consulta.objects.filter(cliente__username=self.request.user__username)
        queryset = queryset.exclude(Q(agenda__dia__lt=localdate()) | 
        Q(agenda__dia=localdate()) & 
        Q(horario__hora__lt=localtime())).order_by('agenda__dia'
        ).order_by('horario__hora')

        return queryset

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

class ConsultaCreateView(generics.CreateAPIView):

    serializer_class = ConsultaSerializerCreate
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
    
        agenda = Agenda.objects.filter(id=request.data['agenda'])
        
        if agenda.exists() == True:
            if agenda.filter(Q(dia__lt=localdate())).exists():
                print(request.data['horario'])
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            agenda_hora_passada = agenda.get(id=request.data['agenda'])
            if agenda_hora_passada.dia == localdate() and datetime.strptime(request.data['horario'],'%H:%M').time() < localtime().time():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            agenda_user = Agenda.objects.get(id=request.data['agenda'])

            consulta_cliente = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
            & Q(horario__hora=request.data['horario']) & Q(cliente__username=self.request.user.username) & Q(isMarcada=True))
            
            if consulta_cliente.exists() == True:
                return Response({'Erro': 'Cliente já marcou uma consulta para este dia e horario'},status=status.HTTP_401_UNAUTHORIZED)

            consulta_ja_marcada = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
            & Q(horario__hora=request.data['horario'])& Q(isMarcada=True))

            if consulta_ja_marcada.exists() == True:
                return Response({'Erro': 'Já existe uma consulta para este dia e horario'},status=status.HTTP_401_UNAUTHORIZED)

            horario = Horario.objects.get(hora=request.data['horario'])
            agenda = Agenda.objects.get(id=request.data['agenda'])
            user = User.objects.get(username=self.request.user.username)
            consulta_criada = Consulta.objects.create(agenda=agenda,cliente=user,
            horario=horario)
            
            return Response({
                'id':consulta_criada.id,
                'dia':consulta_criada.agenda.dia,
                'horario':consulta_criada.horario.hora,
                'data_agendamento':consulta_criada.data_agendamento,
                'medico':{
                    'id': consulta_criada.agenda.medico.id,
                    'crm':consulta_criada.agenda.medico.crm,
                    'nome': consulta_criada.agenda.medico.nome_medico,
                    'especialidade':{
                        'id': consulta_criada.agenda.medico.especialidade_medico.id,
                        'especialidade': consulta_criada.agenda.medico.especialidade_medico.especialidade
                    },
                },
            })
        return Response(status=status.HTTP_404_NOT_FOUND)

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
