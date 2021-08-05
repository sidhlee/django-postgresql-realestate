from django.urls import path
# import the app's views module and assign it to a specific path
from . import views

urlpatterns = [
  # When the request is made to the root path, index function from view's module will run.
  path('', views.index, name='index'), 
  path('about', views.about, name='about'), 
]