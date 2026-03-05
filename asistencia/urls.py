from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.lista_asistencia, name="lista_asistencia"),
    path("descargar/", views.descargar_excel, name="descargar_excel"),
    path("json/", views.lista_asistencia_json, name="lista_asistencia_json"),
]
