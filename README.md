# Python Django Dev to Deployment

A code-along repo for the [Udemy course](https://www.udemy.com/course/python-django-dev-to-deployment/)

## Python Review

### Tuples

- Tuples in python are immutable data structure. You can't reassign values to them once they're initialized.
- You can create a single-value tuple with trailing comma.
- You can't mutate tuples, but you can `delete` them.

## venv

venv is a python module for creating virtual environments.

You can create a virtual environment by:

```bash
# Create a virtual environment in the current directory
python3 -m venv .
```

You can activate the created environment:

```bash
source ./venv/bin/activate
```

Try absolute path if it doesn't work.

Once activated, the python version will default to the version that was used to create this environment.

```bash
(venv) ➜  django-postgresql-realestate python --version
Python 3.9.1
```

Check if the environment is isolated from the main system by:

```bash
pip freeze
# will show no packages installed
```

To leave the environment, you can deactivate it.

```bash
deactivate

pip freeze
# will show all pip packages installed globally
```

## Project setup with Django

1. Activate venv
2. Install Django `pip install django`
3. Create requirements file `pip freeze > requirements.txt`
4. Create `.gitignore`
5. Create `.env` and paste `SECRET_KEY` from `settings.py`
6. Replace secret key inside `settings.py` with env variable.

   ```python
   from decouple import config

   # Access value from .env file
   SECRET_KEY = config('SECRET_KEY')
   ```

7. Init Git
8. Commit

## Django CLI commands

Django creates `manage.py` inside root folder. You can run this file with various options to do server-related tasks.

### Start server

```bash
python manage.py runserver
```

### Create an app

Django app is a sub-module of a project that can function independently and therefore can be easily re-used in other projects.

```bash
python manage.py startapp appname
```

Django app can created in order to:

- Create complete MVC - pages, templates, model, controllers, etc..
- Create just model to be added through admin interface

### Setting up static Assets

First define the following constants in `/project/settings.py` file:

- STATIC_ROOT - absolute path of the folder where Django will collect all the static assets into
- STATIC_URL - URL where the static files from STATIC_ROOT will be served
- STATICFILES_DIRS - The list of paths where Django will look for additional static files aside from each installed app's static folder

Then run `python manage.py collectstatic` to collect all static assets into `STATIC_ROOT`

Django will create `static` folder at the project root and populate it with collected static files as well as assets for Django's admin interface.

## Templating in Django

### Adding templates to apps

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

### Rendering app templates

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

### Customizing admin page

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

### Templating data

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

```text
 <i class="fas fa-user"></i> {{ listing.realtor.name }}</div>
```

### Dynamic routes

You can set the dynamic route inside `urls.py` by setting the url param:

```python
urlpatterns = [
  path('', views.index, name='listings'),
  # listing_id is passed to the listing function as second argument
  path('<int:listing_id>', views.listing, name='listing'),
  path('search', views.search, name='search'),
]
```

Then you take that url param and add to the views function as parameter

```python
def listing(request, listing_id):
  return render(request, 'listings/listing.html')
```

### Django template filter: Humanize

[Humanize](https://docs.djangoproject.com/en/3.2/ref/contrib/humanize/) is the django core app that has many utilities for formatting data inside template. To use Humanize:

1. Include `django.conrib.humanize` in `INSTALLED_APPS` list (settings.py)
2. Load humanize at the top of the template

   ```text
   {% extends 'base.html' %}
   {% load humanize %}

   {% block content %}
   <section id="showcase-inner" class="py-5 text-white">
   ```

3. Pipe the raw data into relevant humanize function

```html
<span class="badge badge-secondary text-white"
  >${{ listing.price | intcomma }}</span
>
```

## Linking app pages

You can use `url` built-in template tag to return an absolute path to the app page.
Django will use the value passed as `name` parameter inside `urls.py` of each app.

```html
<a href="{% url 'index' %}"></a>
```

## Connecting apps to the project

After setting up the app local routes, we can connect apps to the main project by:

1. Installing the app
   Inside `settings.py`, append the apps you want to install to the `INSTALLED_APPS` list

   ```python
   INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps must come after default apps
    'pages.apps.PagesConfig',
    'listings.apps.ListingsConfig',
    ''
   ]
   ```

2. Setting up routes
   include app local routes into the project's `urlpatterns`.

   `btre/urls.py`

   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
      # Linking to the urls of the pages app
      path('',  include('pages.urls')),
      path('listing/',  include('pages.urls')),
      path('admin/', admin.site.urls),
   ]

   ```

## Using PostgreSQL with Django

### Run db server and create db with Postgres.app

1. Download [Postgres.app](https://postgresapp.com/downloads.html) and follow the instruction on "Installing Postgres.app"
2. Double click on `postgres` db to start PostreSQL interactive terminal.
3. Set the password for the user: postgres by:

   ```txt
   postgres=# \password postgres
   ```

4. Create database owned by `postgres` user

   ```txt
   postgres=# CREATE DATABASE btredb OWNER postgres;
   ```

5. Check created db by typing `\l`
6. Exit by `\q`

### Connect db to pgAdmin

1. Install [pgAdmin](https://www.pgadmin.org/)
2. Right click on Servers and select Create > Server
3. Set server name (dbserver), hostname(localhost), Username(postgres), and Password you set for the user, then click on save.
4. Now dbserver is created under Servers which has btredb you created on postgres prompt.
5. Right click on btredb then select Property > Security, then add "postgres" as Grantee and check "All" under Privileges. Save to close window.

### Install PostgreSQL adapter and update settings.py

Inside the virtual environment, install [pycopg](https://pypi.org/project/psycopg2/):

```bash
pip install psycopg2 psycopg2-binary
```

Now change the default database inside the settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'btredb',
        'USER': 'postgres',
        'PASSWORD': <User Password>,
        'HOST': 'localhost'
    }
}
```

### Create models

When you install a django app, `models.py` file is created. You can create the model class inside this file that maps into the database table.

```python
from django.db import models
from datetime import datetime

class Realtor(models.Model):
  name = models.CharField(max_length=200)
  photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
  description = models.TextField(blank=True)
  phone = models.CharField(max_length=20)
  email = models.CharField(max_length=50)
  is_mvp = models.BooleanField(default=False)
  hired_date = models.DateTimeField(default=datetime.now, blank=True)
  def __str__(self):
    return self.name
```

After writing the model class, run `makemigrations` option to create the actual migration file. If there's dependency error, install necessary packages.

```bash
python manage.py makemigrations
```

### Run migrations

Django propagates changes to the models to the database with "migration",
and there are some built-in admin models that need to be migrated into the database.

Run the following command to migrate these models into PostgreSQL tables:

```bash
python manage.py migrate
```

You can check the tables create in your database via pgAdmin.

## Django Admin

### Create super user

In order to login to Django's admin dashboard available at `/admin`, we need to create a staff user (superuser) by running:

```bash
python manage.py createsuperuser
# will prompt to enter username, email, and password
```

### Registering models

You can register app models to create table rows via admin UI.

`realtors/admin.py`

```python
from django.contrib import admin
from .models import Realtor

# Register your models here.
admin.site.register(Realtor)
```

### Customizing admin table

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

### Fetching db records

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

## Trouble Shoot

### Appending app config to `INSTALLED_APPS` results in `ModuleNotFoundError`

When you're registering your app in `settings.py` you need to add the config after all the pre-installed django apps.
`settings.py`

```python

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
# custom apps must come after default apps
'pages.apps.PagesConfig'
]

```

### Prevent prettier from formatting Django-HTML

1. Install Django extension
2. Add the following to `settings.json`

   ```json
   "files.associations": {
      "**/templates/**/*.html": "django-html",
      "**/templates/**/*": "django-txt",
      "**/requirements{/**,*}.{txt,in}": "pip-requirements"
   },
   "[django-html]": {
      "editor.quickSuggestions": {
         "other": true,
         "comments": true,
         "strings": true
      },
      "editor.defaultFormatter": "vscode.html-language-features"
   },
   ```

### Pylint 'Listing has no object member' error

Install `pylint-django` and update vscode settings:

```bash
pip install pylint-django
```

```json
{ "python.linting.pylintArgs": ["--load-plugins=pylint_django"] }
```

## References

- [STATIC_ROOT vs STATIC_URL](https://stackoverflow.com/questions/8687927/difference-between-static-static-url-and-static-root-on-django)
- [Django Migrations: A Primer](https://realpython.com/django-migrations-a-primer/)
- [Django Model field reference](https://docs.djangoproject.com/en/3.2/ref/models/fields/)
