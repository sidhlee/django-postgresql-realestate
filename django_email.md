# Sending email with Django

You can specify the SMTP host and port in the `EMAIL_HOST` and `EMAIL_PORT` settings.
To authenticate to the SMTP server, you need to set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` settings.

`btre/settings.py`

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER='youremail@gmail.com'
EMAIL_HOST_PASSWORD='yourpassword'
EMAIL_USE_TLS = True
```

Then from your POST request handler, you can run `send_email` function.

`contacs/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from contacts.models import Contact

# Create your views here.
def contact(request):
  if request.method == 'POST':
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']

    # Check if the logged-in user has made the inquiry already
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted:
        messages.error(request, 'you have already made an inquiry for this listing')
        return redirect('/listings/' + listing_id)


    contact = Contact(
      listing=listing,
      listing_id=listing_id,
      name=name,
      email=email,
      phone=phone,
      message=message,
      user_id=user_id
    )

    contact.save()

    # Send email
    send_mail(
      'Property Listing Inquiry', # Subject
      'There has been an inquiry for ' + listing +'. Sign into the admin panel for more info', # Body
      config('EMAIL_HOST_USER'), # From address
      [realtor_email, 'sid@sidhlee.com'],
      fail_silently=False
    )

    messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')

    return redirect('/listings/' + listing_id)
```

Check the spam mail bin if you're not seeing the email in your inbox after the mail has been sent.

## Less secure app access

When using gmail's smtp server, you need to go to account settings/security and allow "less secure app access", otherwise your attempt to send an email will be blocked.

## Reference

- [Django Email Documentation](https://docs.djangoproject.com/en/3.2/topics/email/)
