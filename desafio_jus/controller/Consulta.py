from django.http import JsonResponse

def consulta(request):
  if request.method == 'GET':
    consulta = {
      "id": 1,
      "nome": "teste"
    }
    return JsonResponse(consulta)