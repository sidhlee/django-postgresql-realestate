from django.db import models
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from .models import Listing
from listings.choices import price_choices, bedroom_choices, province_choices

def index(request):
  # Query rows in descending order by list_date from listings table 
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

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
  # pk = primary key
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    "listing": listing
  }

  return render(request, 'listings/listing.html', context )

def search(request): 
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      # __icontains allows for case-insensitive keyword search instead of exact match
      queryset_list = queryset_list.filter(description__icontains=keywords)
  
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)
  
  if 'province' in request.GET:
    province = request.GET['province']
    if province:
      queryset_list = queryset_list.filter(province__iexact=province)

  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      # match less than or equal to given bedrooms
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      # match less than or equal to given bedrooms
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'province_choices': province_choices,
    'price_choices': price_choices,
    'bedroom_choices': bedroom_choices,
    'listings': queryset_list,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)