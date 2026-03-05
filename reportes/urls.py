from django.urls import path
from . import views

urlpatterns = [
    path("general/", views.reporte_general, name="reporte_general"),
]
