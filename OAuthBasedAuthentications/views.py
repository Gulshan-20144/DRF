from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from OAuthBasedAuthentications.serializers import OAuthSerializers
from SerializersApp.models import BookStore, Books
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
from user.Pagination import CustomPagination
from rest_framework.views import APIView
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .generatekey import generate_client_id,generate_client_secret

class OauthTokenApiView(APIView):
    authentication_classes=()
    permission_classes=()
    def post(self,request):
        client_id = generate_client_id()
        client_secret =generate_client_secret()
        token_url = 'https://127.0.0.1:8000/api/o/token/'  # Adjust based on your OAuth2 provider URL
        # Create OAuth2 session
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
        access_token = token.get('access_token')
        return Response(access_token)
# Create your views here.
class OAuthView(ModelViewSet):
    queryset=BookStore.objects.all()
    serializer_class=OAuthSerializers
    pagination_class=CustomPagination
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
            data["user"]=User.objects.get(email=data.pop("user")).id
            for book in data.pop("books"):
                if BookStore.objects.filter(books=book).exists():
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
        if not Group.objects.filter(user=user,name="Admin").exists():
            if not self.queryset.filter(id=kwargs.get("pk"),user_id=user).exists():
                raise PermissionDenied("you have not permission to access this user data")
            queryset = self.queryset.filter(id=kwargs.get("pk")).values("id","name", "user", "books", "Qty")
            if not queryset:
                return Response("Data Not Found")
            for lists in queryset:
                lists["user"]=User.objects.filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
                lists["books"]=Books.objects.filter(id=lists["books"]).values("id","name")
            return Response(queryset,status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        user=request.user.id
        if not Group.objects.filter(user=user,name="Admin").exists():
            if not User.objects.filter(id=user).exists():
                raise PermissionDenied("you have not permission to access this user data")    
        queryset = self.filter_queryset(self.get_queryset()).exclude(user__groups__name="Admin").values("id","name", "user", "books", "Qty").order_by("id")
        if not queryset:
            return Response("Data Not Found")
        
        for lists in queryset:
            lists["user"]=User.objects.filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
            lists["books"]=Books.objects.filter(id=lists["books"]).values("id","name")
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(queryset, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            data=request.data
            if not data:
                return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
            data["user"]=User.objects.get(email=data.pop("user")).id
            instance=self.queryset.filter(id=kwargs.get("pk")).first()
            if not instance:
                return Response("Data Not Found",status=status.HTTP_404_NOT_FOUND)
            serializers=self.serializer_class(instance,data=data,partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
            return Response("Data Updated Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        