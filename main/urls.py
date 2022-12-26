from django.urls import path
from main.views import *

urlpatterns = [
    path('',index,name='index'),
    path('categoria/',categoria,name='categoria'),
    path('categoria/editar/<int:pk>/', update_categoria, name='editar_categoria'),
    path('categoria/remover/<int:pk>/', remover_categoria, name='remover_categoria'),
    path('receita/',receita,name='receita'),
    path('receita/editar/<int:pk>/', update_receita, name='editar_receita'),
    path('receita/remover/<int:pk>/', remover_receita, name='remover_receita'),
    path('gasto/',gasto,name='gasto'),
    path('gasto/editar/<int:pk>/', update_gasto, name='editar_gasto'),
    path('gasto/remover/<int:pk>/', remover_gasto, name='remover_gasto'),
]