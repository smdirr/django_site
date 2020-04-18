from django.urls import path
from . import views


app_name = 'cartshop'

urlpatterns = [
    path('', views.cartshop, name='cartshop'),
    path('add', views.add, name='add'),
    path('delete', views.remove, name='remove')
]
