from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.mixins import (CreateModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin)
from rest_framework.viewsets import (ModelViewSet,GenericViewSet,)
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from SerializersApp.models import *
from user.models import User
from HyperLinkSerializersApp .serializers import (BuyBooksHyperSerializer,)
from rest_framework import filters,status
from django_filters.rest_framework import DjangoFilterBackend
from user.permissions import *
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

class HyperSerializerView(CreateModelMixin,RetrieveModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=BookStore.objects.using("default").all()
    serializer_class=BuyBooksHyperSerializer
    # filter_fields = ["name"]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "list":[Admin],
            "retrieve":[Admin|Users]
        }
        permission=[permission() for permission in permission_mapping.get(self.action,[])]
        return permission
       
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
        if not Group.objects.filter(user=user,name="Admin").exists():
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