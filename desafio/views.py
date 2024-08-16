from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from crawler import Crawler

def consulta(request):
  if request.method == 'GET':
    consulta = {
      "id": "1",
      "nome": "João da Silva", 
    }

def index(request):
  return HttpResponse("<h1>Application Running</h1>")