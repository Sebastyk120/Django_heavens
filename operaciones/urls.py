from django.urls import path
from . import views
from .views import MovimientoListView, ItemListView, ItemCreateView, InventariorealTable

urlpatterns = [
    path("", views.home_operaciones2, name="home_operaciones2"),
    path('inventariotr/', views.inventariotr, name='inventariotr'),
    path('mover_item/', InventariorealTable.as_view(), name='mover_item'),
    path('historicos/', MovimientoListView.as_view(), name='historicos'),
    path('recibo_items/', ItemListView.as_view(), name='recibo_items'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
]
