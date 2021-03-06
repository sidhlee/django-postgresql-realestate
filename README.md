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
   You can create `urls.py` inside the app folder and include app local routes into the project's `urlpatterns`.

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
