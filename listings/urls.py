from pages.views import index
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='listings'),
  # listing_id is passed to the listing function as second argument
  path('<int:listing_id>', views.listing, name='listing'),
  path('search', views.search, name='search'),
]