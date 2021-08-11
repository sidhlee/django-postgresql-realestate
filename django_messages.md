# Messages Framework in Django

Django proves the messages framework where you can temporarily store messages in one request and retrieve them for display in a subsequent request.

## Displaying messages

1. Map the message level to the string inside `settings.py` so that we can use it as (a part of) CSS class. The mapped string value will be available at `message.tags`.

   ```python
   from django.contrib.messages import constants as messages

   MESSAGE_TAGS = {
       # set the string representation of the ERROR message level to 'danger'
       messages.ERROR: 'danger',
   }
   ```

2. Create the `_alerts.html` partial that loops through messages and display added messages filtered by the message levels.

   ```php
   {% if messages %}
     {% for message in messages %}
       <div id="message" class="container">
         <div class="alert alert-{{ message.tags }} alert-dismissible text-center" role="alert">
           <button class="close" type="button" data-dismiss="alert"><span aria-hidden="true">&times;</span></button>
           <strong>
           {% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}
             Error:
           {% else %}
             {{ message.tags | title }}
           {% endif %}
           </strong>
           {{ message }}
         </div>
       </div>
     {% endfor %}
   {% endif %}
   ```

3. Add the messages you need to display from the view function

   `accounts.view.py`

   ```python
   from django.shortcuts import render, redirect
   from django.contrib import messages

   # Create your views here.

   def login(request):
     if request.method == 'POST':
       # adding a message to the error level
       messages.error(request, 'Testing error message')

       return redirect('login')
     else:
       return render(request, 'accounts/login.html')
   ```
