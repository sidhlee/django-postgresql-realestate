from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.

def login(request):
  if request.method == 'POST':
    # adding a message to the error level
    messages.error(request, 'Testing error message')    
     
    return redirect('login')
  else:
    return render(request, 'accounts/login.html')

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
          # Log in after register
          # auth.login(request, user)
          # messages.success(request, 'Logged in successfully!')
          # return redirect('index')

          # just save user and redirect to log in
          user.save()
          messages.success(request, 'Registered. Please log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match.')
      return redirect('register')
    
  else:    
    return render(request, 'accounts/register.html')

def logout(request):
  return redirect('index')

def dashboard(request):
  return render(request, 'accounts/dashboard.html')