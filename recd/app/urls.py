from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.home),
     path('course/<int:pk>/', views.read_course, name='read'),
     path('recmmend/',views.recommend_view ,name = "recommend")
    
]