from django.contrib import admin
from django.urls import path
from desafio_jus.controller.Consulta import consulta

urlpatterns = [
    path('admin/', admin.site.urls),
    path("consulta/", consulta)
]
