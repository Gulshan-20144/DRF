from .models import User
from django.core.mail import send_mail
from django.conf import settings

def SendMail(data):
    print(data)
    subject = f'Dear User this issue raise'
    message = f"""Dear {data.first_name} {data.last_name},\n Your account has been blocked for 24 hours due to multiple failed login attempts."""
    recipient_list = [data]
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject, message,from_email,recipient_list)