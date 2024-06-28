from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save
from user.models import User
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.db import transaction
from rest_framework.request import Request

user_updateds={}
@receiver(post_save, sender=User)
@transaction.atomic
def Ragister_singals(sender, instance, created, **kwargs):
    if created:
        user_updateds["created"]=True
        subject = 'Welcome Our Site'
        message = f'You Are Ragister Successfully At My Site'
        recipient_list = [instance.email]
        from_email=settings.EMAIL_HOST_USER
        print(from_email,recipient_list,settings.EMAIL_HOST_PASSWORD,"ffffffffffffffff")
        send_mail(subject, message,from_email,recipient_list)
        

@receiver(user_logged_in,sender=User)
def login_succes(sender, request, **kwargs):
    print(kwargs.get("user"))
    subject = 'Welcome Our Site'
    message = f'You Are Successfully Login At My Site'
    recipient_list = [kwargs.get("user")]
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject, message,from_email,recipient_list)
user_logged_in.connect(login_succes,sender=User)

@receiver(post_save, sender=User)
@transaction.atomic
def user_updated(sender, instance, created, **kwargs):
    if not created:  # Check if the instance is being updated, not created
        if not user_updateds:
            subject = 'Profile Updated'
            message = f'Hi {instance.first_name}, your profile has been updated.'
            recipient_list = [instance.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)