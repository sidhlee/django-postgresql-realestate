from django.db import models
from django.shortcuts import render
from .models import Listing

def index(request):
  # query all rows from listings table
  listings = Listing.objects.all()
  
  context = {
    "listings": listings
  }

  return render(request, 'listings/listings.html', context)

# need to create second parameter matching the name of the param set in urls.py
def listing(request, listing_id):
  return render(request, 'listings/listing.html')

def search(request):
  return render(request, 'listings/search.html')