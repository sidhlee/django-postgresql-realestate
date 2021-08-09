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