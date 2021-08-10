from django.shortcuts import render
from listings.models import Listing

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
  return render(request, 'pages/about.html')
