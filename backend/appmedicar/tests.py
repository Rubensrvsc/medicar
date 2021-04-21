from django.test import TestCase
from rest_framework import status
import requests
# Create your tests here.

class TesteMedicar(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_especialidades(self):
        request = requests.get('http://localhost:8000/especialidades/')
        self.assertEquals(request.status_code,status.HTTP_200_OK)

    def test_medicos(self): 
        request = requests.get('http://localhost:8000/medicos/')
        self.assertEquals(request.status_code,status.HTTP_200_OK)