from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_alumnos, name="lista_alumnos"), 
    path("agregar/", views.agregar_alumno, name="agregar_alumno"), 
    path("editar/<int:fila_id>/", views.editar_alumno, name="editar_alumno"), 
    path("eliminar/<int:fila_id>/", views.eliminar_alumno, name="eliminar_alumno"),
]
