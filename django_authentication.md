# Authentication with Django

Django provides authentication out of the box. All the models related to user and permission are already created.

## Signing up

Signing up is mostly implemented inside the view function as follows:

1. Check if the request method is POST.
2. Assign post payload to variables,
3. Check if username/email already exists in db.
4. If not, create user and save to db.
5. add success message and redirect user to log in.

```python
def register(request):
  if request.method == 'POST':
    # get POST data
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Validate
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.error(request, 'Username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'Email is already registered')
          return redirect('register')
        else:
          user = User.objects.create_user(username=username, password=password, email=email,
           first_name=first_name, last_name=last_name)

          user.save()
          messages.success(request, 'Registered. Please log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match.')
      return redirect('register')

  else:
    return render(request, 'accounts/register.html')

```

You can also log the user in automatically once the signup is done.

```python
if User.objects.filter(email=email).exists():
  messages.error(request, 'Email is already registered')
  return redirect('register')
else:
  user = User.objects.create_user(username=username, password=password, email=email,
    first_name=first_name, last_name=last_name)

  auth.login(request, user)
  messages.success(request, 'Logged in successfully!')
  return redirect('index')
```

## Logging in

Django provides method for authentication and logging in.

```python
from django.contrib import messages, auth

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'Logged in successfully')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')

  else:
    return render(request, 'accounts/login.html')
```

## Logging out

The user logout should be done with POST request because if you use GET, the browser pre-fetch might make request to the logout link.

In Django, logging user out is as simple as calling a method:

```python
def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')
```

Because we're using POST request, the logout link from the frontend should trigger form submit with POST method.  
You can achieve this by putting javaScript inside the link's href:

```php
<li class="nav-item mr-3">
  <a href="javascript:{document.getElementById('logout').submit()}" class="nav-link">
    <i class="fas fa-sign-out-alt"></i> Logout
  </a>
  <form action="{% url 'logout' %}" method="POST" id="logout">
    <!-- csrf protection provided by django -->
    {% csrf_token %}
    <input type="hidden">
  </form>
</li>
```
