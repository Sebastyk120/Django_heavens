from django.urls import path
from . import views

urlpatterns = [
    path('home_inventario_tr', views.inventariotr, name='homeinventariotr'),
    path('intentariotr_items_list', views.InventarioRealListView.as_view(), name='inventariotrlist'),
    path('intentariotr_items_mover', views.InventarioCreateView.as_view(), name='inventariotrmover'),
    path('historico_items', views.MovimientoListView.as_view(), name='historicos'),
    path('recibo_items_list', views.ItemListView.as_view(), name='reciboitemslist'),
    path('recibo_items_create', views.ItemCreateView.as_view(), name='reciboitemscreate'),
<<<<<<< HEAD
=======
    path('home_muestreo', views.muestreo, name='homemuestreo'),
>>>>>>> b7f5c408a72c6bf41db92399e252dd7048570347
    path('historico_muestreo_items', views.MuestreoHistoricoListView.as_view(), name='historicos_muestreo'),
    path('muestreo_items_list', views.MuestreoListView.as_view(), name='muestreoitemslist'),
    path('muestreo_items_create', views.MuestreoCreateView.as_view(), name='muestreoitemscreate'),
]
