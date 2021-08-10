from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor

# Create your views here.

def index(request):
  ''' 
  Renders html inside templates folder
  '''
  # fetch listings in descending order by list date
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

  context = {
    'listings': listings
  }
  return render(request, 'pages/index.html', context)

def about(request):
  realtors = Realtor.objects.order_by('-hired_date')
  mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

  context = {
    "realtors": realtors,
    "mvp_realtors": mvp_realtors
  }

  return render(request, 'pages/about.html', context)
