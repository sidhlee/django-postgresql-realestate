from django.db import models
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from .models import Listing

def index(request):
  # Query rows in descending order by list_date from listings table 
  listings = Listing.objects.order_by('-list_date')

  # Create new paginator instance with listings data and items per page set to 3
  paginator = Paginator(listings, 6)
  # Get requested page number
  page_number = request.GET.get('page')

  # Get listings for the given page
  paged_listings = paginator.get_page(page_number)
  
  context = {
    "listings": paged_listings
  }

  return render(request, 'listings/listings.html', context)

# need to create second parameter matching the name of the param set in urls.py
def listing(request, listing_id):
  return render(request, 'listings/listing.html')

def search(request):
  return render(request, 'listings/search.html')