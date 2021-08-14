# Templating with Django

## Adding templates to apps

When you create(start) app, Django will populate the app folder with `views.py` file. Inside this file, you will define functions that render pages inside `templates` folder using Django's `render` function.

`pages/views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
  '''
  Renders html inside templates folder
  '''
  return render(request, 'pages/index.html')

def about(request):
  return render(request, 'pages/about.html')


```

## Rendering app templates

After creating (staring) app and defining render function in `views.py`, you can assign the render functions to the corresponding routes by:

1. Create `urls.py` file inside the app
2. Create `urlpatterns` assigned to the list of paths connecting views to the routes

`pages/urls.py`

```python
from django.urls import path
# import the app's views module and assign it to a specific path
from . import views

urlpatterns = [
  # When the request is made to the root path, index function from view's module will run.
  path('', views.index, name='index'),
  path('about', views.about, name='about'),
]
```

## Adding internal links

You can use `url` built-in template tag to return an absolute path to the app page.
Django will use the value passed as `name` parameter inside `urls.py` of each app.

```html
<a href="{% url 'index' %}"></a>
```

## Customizing admin page

You can extend the base template for admin page and add blocks for individual partials to overwrite them.

```jinja
{% extends 'admin/base.html' %}
{% load static %}

{% block branding %}
  <h1 id="head">
    <img class="brand_img" src="{% static 'img/logo.png' %}" alt="BT Real Estate"  height="50">
    Admin Area
  </h1>
{% endblock %}
```

You can also add `extrastyle` block to add stylesheet for specific template. The style link is pointing to the `/static/css` inside your project folder (`/btre/`).

```jinja
{% block extrastyle %}
  <link rel="stylesheet" href="{% static 'css/admin.css' %}">
{% endblock %}
```

## Templating data

We can create the "context" dictionary and pass it to the render function after the template path.

```python
def index(request):
  # query all rows from listings table
  listings = Listing.objects.all()

  context = {
    "listings": listings
  }

  return render(request, 'listings/listings.html', context)

```

You can access fields of the foreign table simply with the dot notation.

```php
 <i class="fas fa-user"></i> {{ listing.realtor.name }}</div>
```

## Django template filter: Humanize

[Humanize](https://docs.djangoproject.com/en/3.2/ref/contrib/humanize/) is the django core app that has many utilities for formatting data inside template. To use Humanize:

1. Include `django.conrib.humanize` in `INSTALLED_APPS` list (settings.py)
2. Load humanize at the top of the template

   ```php
   {% extends 'base.html' %}
   {% load humanize %}

   {% block content %}
   <section id="showcase-inner" class="py-5 text-white">
   ```

3. Pipe the raw data into relevant humanize function

   ```php
   <span class="badge badge-secondary text-white">
     ${{ listing.price | intcomma }}
   </span>
   ```
