from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_operaciones2, name="home_operaciones2"),
    path('inventariotr/', views.inventariotr, name='inventariotr'),
    path('mover_item/', views.mover_item, name='mover_item')
]
