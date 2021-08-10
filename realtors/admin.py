from django.contrib import admin
from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'email', 'hired_date', 'is_mvp')
  list_display_links = ('id', 'name')
  search_fields = ('name',)
  list_per_page = 25
  list_editable = ('is_mvp',)

# Register your models here.
admin.site.register(Realtor, RealtorAdmin)