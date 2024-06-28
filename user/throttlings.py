from django.http import HttpResponse
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import socket
from user.models import User
from SerializersApp.models import UserBlock
from .send_mails import SendMail

#class based throttling by inherting basethrotle 
class IPBasedRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = self.get_client_ip(request)
        cache_key = f'failed_login_ip_block:{ip}'
        try:
            user_ip = UserBlock.using("default").objects.get(system_ip=ip)
            if user_ip.timestamps and user_ip.timestamps > timezone.now():
                user=User.objects.using("default").get(email=request.data["email"])
                SendMail(user)
                return False
        except UserBlock.DoesNotExist:
            pass    
        requests_count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, requests_count, timeout=settings.THROTTLE_TIMEOUT)
        max_requests = settings.MAX_REQUESTS_PER_IP
        if requests_count == max_requests:
            user= User.objects.get(email=request.data.get("email"))
            block, created = UserBlock.objects.using("default").get_or_create(
                                user=user,
                                system_ip=ip,
                                defaults={'blocked_until': timezone.now() + timedelta(minutes=settings.THROTTLE_TIMEOUT)})
            if not created:
                if block.timestamps < timezone.now():
                    block.timestamps = timezone.now() + timedelta(minutes=2)
                    block.save()
            SendMail(user)
            return False
        return True
    
    def wait(self):
        """
        Optionally, return a recommended number of seconds to wait before
        the next request.
        """
        return settings.THROTTLE_TIMEOUT

    def get_client_ip(self, request):
        try:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            return IPAddr
        except socket.error:
            return None
        
#functions based  or decorater based throttling
def block_user_attempts(max_attempts):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            ip_address = request.META.get('REMOTE_ADDR')
            user = User.objects.get(email=request.data.get("email"))
            # Check if there are previous failed attempts
            if not user.check_password(request.data["password"]):
                failed_attempts = UserBlock.objects.using("default").filter(user=user, system_ip=ip_address)
                if failed_attempts.exists():
                    last_attempt = failed_attempts.latest('timestamps')
                    if last_attempt.timestamps and last_attempt.timestamps > timezone.now():
                        if last_attempt.count_num >= max_attempts:
                            SendMail(user)
                            return send_blocked_response()
                        else:
                            last_attempt.count_num += 1
                            last_attempt.save()
                    else:
                        # Reset attempts if more than 24 hours have passed
                        last_attempt.count_num = 1
                        last_attempt.timestamps = timezone.now() + timedelta(minutes=settings.THROTTLE_TIMEOUT)
                        last_attempt.save()
                else:
                    UserBlock.objects.using("default").create(user=user, system_ip=ip_address, count_num=1, timestamps=timezone.now() + timedelta(minutes=settings.THROTTLE_TIMEOUT))
            # Call the original view function with self and request
            return view_func(self, request, *args, **kwargs)

        return wrapped_view

    return decorator

def send_blocked_response():
    # Placeholder function to return a response when user is blocked
    return Response("Too many failed login attempts. Your account is blocked for 24 hours.", status=status.HTTP_429_TOO_MANY_REQUESTS)
