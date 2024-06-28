from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from ViewSetApp.serializers import ViewsetSerializers
from SerializersApp.models import BookStore
from user.models import User
from SerializersApp.models import Books
from user.permissions import Admin, Users
from .models import *
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from user.Pagination import CustomPagination

# Create your views here.
class UploadDataViewsetView(ViewSet):
    queryset=BookStore.objects.using("default").all()
    serializer_class=ViewsetSerializers
    filter_fields=["name"]
    search_fields=["name","user_id__first_name"]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "list":[Admin],
            "retrieve":[Admin|Users],
            "partial_update":[Admin | Users],
            "create":[Admin],
            "delete":[Admin]
        }
        permission=[permission() for permission in permission_mapping.get(self.action,[])]
        return permission
    @swagger_auto_schema(request_body=ViewsetSerializers)
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
        queryset = BookStore.objects.using("default").all().exclude(user__groups__name="Admin").values("id","name", "user", "books", "Qty").order_by("id")
        if not queryset:
            return Response("Data Not Found")
        
        for lists in queryset:
            lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
            lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, self)
        return paginator.get_paginated_response(paginated_queryset)


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
    
    def destroy(self ,request,*args,**kwargs):
        try:
            instance=BookStore.objects.using("default").filter(id=kwargs.get("pk")).first()
            if instance:
                instance.delete()
                return Response("Data delete Succesfully",status=status.HTTP_204_NO_CONTENT)
            raise Exception("Data already delete Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)