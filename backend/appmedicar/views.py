from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
# Create your views here.

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
