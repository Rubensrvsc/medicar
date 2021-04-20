from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
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
