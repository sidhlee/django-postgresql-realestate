# Routing in Django

Here's the typical workflow for setting up page routings in Django:

1. Install app with `python manage.py startapp mypage`
2. Register the app inside `settings.py` by adding to the `INSTALLED_APPS` list

   ```python
   INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'django.contrib.humanize',
     # custom apps must come after default apps
     'pages.apps.PagesConfig',
     'listings.apps.ListingsConfig',
     'realtors.apps.RealtorsConfig',
     'accounts.apps.AccountsConfig'
   ]
   ```

3. Create `urls.py` inside the installed app folder and create `urlpatterns` list. Inside the list, you'll add individual routes by calling `path` function passing in the route url, matching view function from the `views` module, and the name of the route, which we'll use inside the template with `url` template tag.
   `accounts/urls.py`

   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
   path('login', views.login, name='login'),
   path('register', views.register, name='register'),
   path('logout', views.logout, name='logout'),
   path('dashboard', views.dashboard, name='dashboard')
   ]
   ```

4. Register the app's urls to the project folder's `urls.py` file.
   `btre/urls.py`

   ```python
   urlpatterns = [
     # Linking to the urls of the pages app
     # path('url', include('app_name.urls'))
     path('',  include('pages.urls')),
     path('listings/',  include('listings.urls')),
     path('accounts/', include('accounts.urls')),
     path('admin/', admin.site.urls),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

5. Create the actual view functions inside `views.py`

   `accounts/views.py`

   ```python
   from django.shortcuts import render, redirect

   # Create your views here.

   def login(request):
     return render(request, 'accounts/login.html')

   def register(request):
     return render(request, 'accounts/register.html')

   def logout(request):
     return redirect('index')

   def dashboard(request):
     return render(request, 'accounts/dashboard.html')
   ```

6. Go to the template files and use the route name as the link href

   ```php
   <ul class="navbar-nav">
     <li
       {% if '/' == request.path %}
         class="nav-item active mr-3"
       {% else %}
         class="nav-item mr-3"
       {% endif %}
     >
       <a class="nav-link" href="{% url 'index' %}">Home</a>
     </li>
     <li
       {% if '/about' == request.path %}
         class="nav-item active mr-3"
       {% else %}
         class="nav-item mr-3"
       {% endif %}
     >
       <a class="nav-link" href="{% url 'about' %}">About</a>
     </li>
     <li
       {% if 'listings' in request.path %}
         class="nav-item active mr-3"
       {% else %}
         class="nav-item mr-3"
       {% endif %}
     >
       <a class="nav-link" href="{% url 'listings' %}">Featured Listings</a>
     </li>
   </ul>
   ```

## Dynamic routes

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
