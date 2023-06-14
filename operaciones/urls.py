from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_operaciones, name='home_operaciones2'),
]
