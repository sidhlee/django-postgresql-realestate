from django.urls import path

from . import views

urlpatterns = [
  # root path
  path('', views.index, name='index') 
]