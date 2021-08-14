# Django Admin

Django provides built-in admin page where you can manage user privileges and database tables.

## Create super user

In order to login to Django's admin dashboard available at `/admin`, we need to create a staff user (superuser) by running:

```bash
python manage.py createsuperuser
# will prompt to enter username, email, and password
```

## Registering models

You can register app models to create table rows via admin UI.

`realtors/admin.py`

```python
from django.contrib import admin
from .models import Realtor

# Register your models here.
admin.site.register(Realtor)
```

## Customizing admin table

You can customize admin table by creating ModelAdmin class and
add it when you're registering the model inside `admin.py`

`/listings/admin.py`

```python
from django.contrib import admin
from .models import Listing


# Create ModelAdmin class to customize admin table
class ListingAdmin (admin.ModelAdmin):
  # show these columns on the table
  list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
  # make these columns link to the corresponding item
  list_display_links = ('id', 'title')
  # add filters by the following columns
  list_filter = ('realtor',)
  # make the column directly editable
  list_editable = ('is_published',)
  # enable search on the following fields (columns)
  search_fields = ('title', 'description', 'address', 'city', 'province', 'postalcode', 'price')
  # set pagination
  list_per_page = 25

# Register models
admin.site.register(Listing, ListingAdmin)

```

## Fetching db records

Django allows you to import installed app's files from any other app. For example you can import listings app's `Listing` model from pages app like so:

'pages/views.py`

```python
from django.shortcuts import render
from listings.models import Listing
```

Then you can call the models method to make queries against the matching table from the database. Usually you add the fetched table to a context dictionary and pass that to the render function.

```python
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

```
