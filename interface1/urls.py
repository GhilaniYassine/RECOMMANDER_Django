from django.urls import path
from . import views

app_name = 'interface1'

urlpatterns = [
    path('', views.index, name='index'),
]