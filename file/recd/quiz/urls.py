

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('quiz/', views.take_quiz, name='take_quiz'),
    path('results/', views.results, name='results'),
]