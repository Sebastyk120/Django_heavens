from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_operaciones, name='home_operaciones2'),
    path('mover_item/', views.mover_item, name='mover_item')
]
