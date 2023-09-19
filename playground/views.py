import contextlib
from django.shortcuts import render
from django.core.mail import *
from .tasks import notify_customers


def say_hello(request):

    # with contextlib.suppress(BadHeaderError):
    #     # mail_admins('subject', 'messege', html_message='message 2')
    #     # send_mail('subject', 'messege','', ['moler@gmail.com'])
    #     message = EmailMessage('subject', 'messege', '', ['moler@gmail.com'])
    #     message.send()
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Mosh'})
