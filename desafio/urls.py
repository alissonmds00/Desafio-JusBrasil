from django.urls import path
from desafio.views import consulta, index

urlpatterns = [
  path('consulta', consulta, name="consulta"),
  path('', index)
]