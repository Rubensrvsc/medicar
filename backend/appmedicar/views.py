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
    
    def get_queryset(self):
        medico_params = self.request.query_params.getlist('medico',None)
        especialidade_params = self.request.query_params.getlist('especialidade',None)
        data_inicio = self.request.query_params.get('data_inicio',None)
        data_fim = self.request.query_params.get('data_fim',None)

        agenda = Agenda.objects.all()
        agenda = Agenda.objects.filter(Q(dia__gte=localdate()) | Q(dia=localdate()) ).order_by('dia')
        for i in agenda.filter(Q(dia__gte=localdate())): 
            if i.dia == localdate():
                hora_passada=0
                hora_marcadas= i.consulta_agenda.filter(Q(isMarcada=True) & Q(horario__hora__gt=localtime())).count()
                hora_passada = i.horario.filter(Q(hora__lt=localtime()) & Q(agenda__dia=localdate())).count()
                hora_agenda= i.horario.count() 
   
                if hora_marcadas+ hora_passada == hora_agenda: 
                    agenda=agenda.exclude(id=i.id) 
            hora_marcadas= i.consulta_agenda.filter(Q(isMarcada=True)).count() 

            hora_agenda= i.horario.count() 
  
            if hora_marcadas == hora_agenda: 
                agenda=agenda.exclude(id=i.id) 
        if medico_params:
            condition_medico = Q()
            for m in medico_params:
                condition_medico |= Q(medico=m)
            agenda = agenda.filter(condition_medico)
        if especialidade_params:
            condition_especialidade = Q()
            for e in especialidade_params:
                condition_especialidade |= Q(medico__especialidade_medico=e)
            agenda = agenda.filter(condition_especialidade)
        
        if data_inicio and data_fim:
            agenda = agenda.filter(Q(dia__range=[data_inicio,data_fim]))
        
        return agenda.all()

class ConsultaCreateView(generics.CreateAPIView):

    serializer_class = ConsultaSerializerCreate

    def post(self, request, *args, **kwargs):
    
        agenda = Agenda.objects.filter(id=request.data['agenda'])
        
        if agenda.exists() == True:
            if agenda.filter(Q(dia__lt=localdate())).exists():
                return Response({'Erro': 'Agenda é de um dia passado'},status=status.HTTP_401_UNAUTHORIZED)
            agenda_hora_passada = agenda.get(id=request.data['agenda'])
            if agenda_hora_passada.dia == localdate() and datetime.strptime(request.data['horario'],'%H:%M').time() < localtime().time():
                return Response({'Erro': 'Agenda do dia de hoje mas o horário já passou'},status=status.HTTP_400_BAD_REQUEST)

            agenda_user = Agenda.objects.get(id=request.data['agenda'])

            consulta_cliente = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
            & Q(horario__hora=request.data['horario']) & Q(cliente__username=self.request.user.username) & Q(isMarcada=True))
            
            if consulta_cliente.exists() == True:
                return Response({'Erro': 'Cliente já marcou uma consulta para este dia e horario'},status=status.HTTP_401_UNAUTHORIZED)

            consulta_ja_marcada = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
            & Q(horario__hora=request.data['horario'])& Q(isMarcada=True))

            if consulta_ja_marcada.exists() == True:
                return Response({'Erro': 'Já existe uma consulta para este dia e horario'},status=status.HTTP_401_UNAUTHORIZED)
            
            if agenda_user.horario.filter(hora=request.data['horario']).exists()==False:
                return Response({'Erro': 'Esse horario não existe nessa agenda'},status=status.HTTP_404_NOT_FOUND)

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
                        'especialidade': consulta_criada.agenda.medico.especialidade_medico.nome_especialidade
                    },
                },
            })
        return Response(status=status.HTTP_404_NOT_FOUND)

class DesmarcarConsultaView(generics.DestroyAPIView):
    serializer_class = DesmarcarConsultaSerializer
    queryset = Consulta.objects.all()

    def destroy(self, request,id):
        consulta = Consulta.objects.filter(id=id)
        if consulta.exists():
            consulta_usuario=consulta.filter(Q(cliente__username=self.request.user.username) & Q(id=id))
            if consulta_usuario.exists():
                consulta_horario = consulta_usuario.filter(Q(agenda__dia__lt=localdate())  & Q(isMarcada=True)
                | Q(agenda__dia=localdate()) & Q(horario__hora__lte=localtime()) & Q(isMarcada=True) )
                
                if consulta_horario.exists():
                    return Response({'Erro':'consulta já passou'},status=status.HTTP_404_NOT_FOUND)


                return Response(consulta_usuario.filter(id=id).first().delete(),status=status.HTTP_200_OK)
            
            return Response({'Erro':'Essa consulta não foi marcada pelo usuário logado'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Erro':'Essa consulta não existe'},status=status.HTTP_404_NOT_FOUND)


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
