from celery import shared_task
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from .serializers import RagisterSerializers,ChangePasswordSerializer # Adjust import as per your project structure

@shared_task()
def register_user_task(data):
    try:
        serializer = RagisterSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'message': 'User registered successfully'}
    except ValidationError as e:
        return {'success': False, 'error': str(e)}
    
@shared_task()
def change_user_password_task(data,user):
    try:
        serializers=ChangePasswordSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            users=User.objects.using("default").get(id=user)
            if users.check_password(data["current_password"]):
                users.set_password(data["password"])
                users.save()
                return {'success': True, 'message': "Chenge Password Successfully"}
            else:
                raise Exception("Current Password Wrong")
    except ValidationError as e:
        return {'success': False, 'error': str(e)}
    except User.DoesNotExist:
        return {'success': False, 'error': "User not found with the given ID"}
    except Exception as f:
        return {'success': False, 'error': str(f)}