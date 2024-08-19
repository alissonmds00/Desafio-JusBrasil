from django.urls import path
from desafio.views.consulta import ConsultaView

urlpatterns = [
    path('processos/<str:numero_processo>', ConsultaView.as_view(), name="consulta"),
]