from django.urls import path
from . import views
from .views import MovimientoListView, ItemListView, ItemCreateView, InventarioRealListView, InventarioCreateView

urlpatterns = [
    path('home_inventario_tr', views.inventariotr, name='homeinventariotr'),
    path('intentariotr_items_list', InventarioRealListView.as_view(), name='inventariotrlist'),
    path('intentariotr_items_mover', InventarioCreateView.as_view(), name='inventariotrmover'),
    path('historico_items', MovimientoListView.as_view(), name='historicos'),
    path('recibo_items_list', ItemListView.as_view(), name='reciboitemslist'),
    path('recibo_items_create', ItemCreateView.as_view(), name='reciboitemscreate'),
]
