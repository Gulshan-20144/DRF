from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView

from user.task import register_user_task,change_user_password_task
from .serializers import RagisterSerializers,LoginTokenSerializers,ChangePasswordSerializer
from .models import *
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView,TokenViewBase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from user.permissions import Admin,Users,IsAuthenticated
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.exceptions import PermissionDenied
from user.throttlings import IPBasedRateThrottle,block_user_attempts

# Create your views here.
class RagistrationsApiView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class=RagisterSerializers
    @swagger_auto_schema(request_body=RagisterSerializers)
    def post(self,request):
        try:
            datas=request.data
            result=register_user_task.delay(datas)
            task_result = result.get()
            if task_result['success']:
                return Response(task_result['message'], status=status.HTTP_200_OK)
            else:
                return Response(task_result['error'], status=status.HTTP_400_BAD_REQUEST)
            # serializers=self.serializer_class(data=data)
            # if serializers.is_valid(raise_exception=True):
            #     serializers.save()
            #     return Response("User Ragister Successfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(TokenObtainPairView):
    serializer_class=LoginTokenSerializers
    authentication_classes=(JWTAuthentication,)

    @block_user_attempts(max_attempts=5)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenRefreshView(TokenViewBase):

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER
    def post(self, request, *args, **kwargs):
        refresh=request.data.get("refresh")
        if not refresh:
            return Response("this field is requird")
        return super().post(request, *args, **kwargs)
    
class ChangePasswordView(TokenObtainPairView):
   authentication_classes=[JWTAuthentication]
   permission_classes=[IsAuthenticated]
   def patch(self,request):
       try:
            datas=request.data
            result = change_user_password_task.delay(datas, request.user.id)
            task_result = result.get()
            if task_result['success']:
                return Response(task_result['message'], status=status.HTTP_200_OK)
            else:
                return Response(task_result['error'], status=status.HTTP_400_BAD_REQUEST)  # Wait for the Celery task to complete and get the result
       except Exception as e:
           return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
            