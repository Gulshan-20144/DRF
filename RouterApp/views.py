from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from user.Pagination import CustomPagination
from RouterApp.serializers import DistibuterSerializers, RouterAppSerializers
from SerializersApp.models import BookStore, Books
from rest_framework.views import APIView
from user.models import User
from user.permissions import Admin, Users
from .models import *
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class UploadDataRouterView(ModelViewSet):
    queryset=BookStore.objects.using("default").all()
    serializer_class=RouterAppSerializers
    filter_fields=["name"]
    search_fields=["name","user_id__first_name"]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "list":[Admin],
            "retrieve":[Admin|Users],
            "partial_update":[Admin | Users],
            "create":[Admin]
        }
        permission=[permission() for permission in permission_mapping.get(self.action,[])]
        return permission
    def create(self, request, *args, **kwargs):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.using("default").get(email=data.pop("user")).id
            for book in data.pop("books"):
                if BookStore.objects.using("default").filter(books=book).exists():
                    return Response("This book Id is Already Register Beacause this make OneToOne relationship")
                data["books"]=book 
                serializers=self.serializer_class(data=data)
                if serializers.is_valid(raise_exception=True):
                    serializers.save()
            name=data.get("name")
            return Response(f"Successfully Books buy from username {name}")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, *args, **kwargs):
        user=request.user.id
        if not Group.objects.using("default").filter(user=user,name="Admin").exists():
            if not self.queryset.filter(id=kwargs.get("pk"),user_id=user).exists():
                raise PermissionDenied("you have not permission to access this user data")
        queryset = self.queryset.filter(id=kwargs.get("pk")).values("id","name", "user", "books", "Qty")
        if not queryset:
            return Response("Data Not Found")
        for lists in queryset:
            lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
            lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
        return Response(queryset,status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        user=request.user.id
        if not Group.objects.using("default").filter(user=user,name="Admin").exists():
            if not User.objects.using("default").filter(id=user).exists():
                raise PermissionDenied("you have not permission to access this user data")    
        queryset = self.filter_queryset(self.get_queryset()).exclude(user__groups__name="Admin").values("id","name", "user", "books", "Qty").order_by("id")
        if not queryset:
            return Response("Data Not Found")
        
        for lists in queryset:
            lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
            lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(queryset, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.using("default").get(email=data.pop("user")).id
            instance=self.queryset.filter(id=kwargs.get("pk")).first()
            if not instance:
                return Response("Data Not Found",status=status.HTTP_404_NOT_FOUND)
            serializers=self.serializer_class(instance,data=data,partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
            return Response("Data Updated Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
class RouterDataView(ListCreateAPIView,RetrieveUpdateDestroyAPIView):
    queryset=BookStore.objects.using("default").all()
    serializer_class=RouterAppSerializers
    filter_fields=["name"]
    search_fields=["name","user_id__first_name"]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "post":[Admin],
            "get":[Admin|Users],
            "patch":[Admin | Users]
        }
        permission=[permission() for permission in permission_mapping.get(self.request.method.lower(),[])]
        return permission
    @swagger_auto_schema(request_body=RouterAppSerializers)
    def post(self,request):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.using("default").get(email=data.pop("user")).id
            for book in data.pop("books"):
                if BookStore.objects.using("default").filter(books=book,is_deleted=False).exists():
                    return Response("This book Id is Already Register Beacause this make OneToOne relationship")
                data["books"]=book
            serializers=self.serializer_class(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return Response("User Ragister Successfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,*args,**kwargs):
        user=request.user.id
        if not kwargs.get("pk") and Group.objects.using("default").filter(user=user,name="Admin").exists():  
            data = self.filter_queryset(self.get_queryset()).values("id","name", "user", "books", "Qty")
            if not data:
                return Response("Data Not Found")
            return Response(data,status=status.HTTP_200_OK)
        else:
            if not Group.objects.using("default").filter(user=user,name="Admin").exists():
                if not BookStore.objects.using("default").filter(id=kwargs.get("pk"),user=user).exists():
                    raise PermissionDenied("you have not permission to access this user data")
            data=BookStore.objects.using("default").filter(id=kwargs.get("pk")).values("id","name","user","books","Qty")
            if not data:
                return Response("Data Not Found")
            return Response(data,status=status.HTTP_200_OK)
        
    def patch(self ,request,*args,**kwargs):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.using("default").get(email=data.pop("user")).id
            instance=BookStore.objects.using("default").filter(id=kwargs.get("pk")).first()
            if not instance:
                return Response("Data Not Found",status=status.HTTP_404_NOT_FOUND)
            serializers=self.serializer_class(instance,data=data,partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
            return Response("Data Updated Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
class RouterApiView(APIView):
    
    serializer_class=RouterAppSerializers
    
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "post":[Admin],
            "get":[Admin|Users],
            "patch":[Admin | Users]
        }
        permission=[permission() for permission in permission_mapping.get(self.request.method.lower(),[])]
        return permission
        
    def get(self,request,*args,**kwargs):
        user=request.user.id
        if not kwargs.get("pk") and Group.objects.using("default").filter(user=user,name="Admin").exists():  
            data = BookStore.objects.using("default").all().values("id","name", "user", "books", "Qty")
            if not data:
                return Response("Data Not Found")
            return Response(data,status=status.HTTP_200_OK)
        else:
            if not Group.objects.using("default").filter(user=user,name="Admin").exists():
                if not BookStore.objects.using("default").filter(id=kwargs.get("pk"),user=user).exists():
                    raise PermissionDenied("you have not permission to access this user data")
            data=BookStore.objects.using("default").filter(id=kwargs.get("pk")).values("id","name","user","books","Qty")
            if not data:
                return Response("Data Not Found")
            return Response(data,status=status.HTTP_200_OK)
        
    def patch(self ,request,*args,**kwargs):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.using("default").get(email=data.pop("user")).id
            instance=BookStore.objects.using("default").filter(id=kwargs.get("pk")).first()
            serializers=self.serializer_class(instance,data=data,partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
            return Response("Data Updated Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
class DistibuterView(ModelViewSet):
    queryset=Distibuter.objects.using("user_db").all()
    serializer_class=DistibuterSerializers
    pagination_class=CustomPagination
    permission_classes=()
    authentication_classes=()
    filter_fields=["name"]
    search_fields=["name"]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]