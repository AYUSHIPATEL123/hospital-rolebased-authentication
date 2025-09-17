from celery import shared_task
from time import sleep
from .models import User
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
@shared_task
def add(x, y):
    sleep(60)
    return x+y


@shared_task
def send_email(user_id):
    # print("hellooo,.....")
    user = User.objects.get(pk=user_id)
    subject = "you account has been created successfully"
    message = f"welcome {user.first_name} {user.last_name} to our website and\nyou are our {user.role} now."
    send_email_massege = EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,to=[user.email])
    send_email_massege.send(fail_silently=False)
    return None  

    
    
    