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

@shared_task
def daily_reminder_email(user_id):
    user = User.objects.get(pk=user_id)
    subject = "Daily Reminder"
    message = f"Hello {user.first_name}, stay engaged with your work.stay active login to this wensite."
    send_email_massege = EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,to=[user.email])
    send_email_massege.send(fail_silently=False)
    return None
@shared_task
def weekly_reminder_email(user_id):
    user = User.objects.get(pk=user_id)
    subject = "Weekly Reminder"
    message = f"Hello {user.first_name}, please don't forget to check your tasks and complete them on time."
    send_email_massege = EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,to=[user.email])
    send_email_massege.send(fail_silently=False)
    return None

@shared_task
def daily_reminder():
    users = User.objects.all()
    for user in users:
        daily_reminder_email.delay(user.id)
    return None

@shared_task
def weekly_reminder():
    users = User.objects.all()
    for user in users:
        weekly_reminder_email.delay(user.id)
    return None