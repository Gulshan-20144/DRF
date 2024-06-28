from rest_framework.request import Request
from rest_framework.views import APIView
from FunctionBasedCrudApp.serializers import functionViewSerializers
from SerializersApp.models import BookStore, Books
from user.models import User
from user.permissions import Admin, IsAuthenticated, Users
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from user.Pagination import CustomPagination
from rest_framework.decorators import api_view,authentication_classes,permission_classes


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bookstore_detail(request, pk):
    try:
        user = request.user.id       
        # Check if user is admin or has permission to access user data
        if not Group.objects.using("default").filter(user=user, name="Admin").exists():
            if not BookStore.objects.using("default").filter(user=user,id=pk).exists():
                raise PermissionDenied("You do not have permission to access this user's data")   
            
            queryset = BookStore.objects.using("default").filter(id=pk).values("id", "name", "user", "books", "Qty")     
            if not queryset:
                return Response("Data Not Found", status=status.HTTP_404_NOT_FOUND)         
            # Fetch related user and books information for each BookStore entry
            for item in queryset:
                item["user"] = User.objects.using("default").filter(id=item["user"]).values("id", "first_name", "last_name", "email", "gender", "contact", "dob", "groups__name").first()
                item["books"] = Books.objects.using("default").filter(id=item["books"]).values("id", "name").first()         
            return Response(queryset, status=status.HTTP_200_OK)
        else:
            queryset = BookStore.objects.using("default").filter(id=pk).values("id", "name", "user", "books", "Qty")     
            if not queryset:
                return Response("Data Not Found", status=status.HTTP_404_NOT_FOUND)         
            # Fetch related user and books information for each BookStore entry
            for item in queryset:
                item["user"] = User.objects.using("default").filter(id=item["user"]).values("id", "first_name", "last_name", "email", "gender", "contact", "dob", "groups__name")
                item["books"] = Books.objects.using("default").filter(id=item["books"]).values("id", "name").first()            
            return Response(queryset, status=status.HTTP_200_OK)
    # Handle case where user is an admin
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bookstore_list(request):
    try:
        user = request.user.id  
        if Group.objects.using("default").filter(user=user, name="Admin").exists():
            queryset = BookStore.objects.using("default").all().exclude(user__groups__name="Admin").values("id","name", "user", "books", "Qty").order_by("id")
            if not queryset:
                return Response("Data Not Found")            
            for lists in queryset:
                lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
                lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            return paginator.get_paginated_response(paginated_queryset)
        else:
            raise PermissionDenied("You do not have permission to access list data")
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bookstore_partial_update(request, pk):
    try:
        data=request.data
        if not data:
            return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
        data["user"]=User.objects.using("default").get(email=data.pop("user")).id
        instance=BookStore.objects.using("default").filter(id=pk).first()
        if not instance:
            return Response("Data Not Found",status=status.HTTP_404_NOT_FOUND)
        serializers=functionViewSerializers(instance,data=data,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
        return Response("Data Updated Succesfully")
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bookstore_create(request):
    try:
        data=request.data
        if not data:
            return Response("Input Data Is Required",status=status.HTTP_400_BAD_REQUEST)
        data["user"]=User.objects.using("default").get(email=data.pop("user")).id
        for book in data.pop("books"):
            if BookStore.objects.using("default").filter(books=book).exists():
                return Response("This book Id is Already Register Beacause this make OneToOne relationship")
            data["books"]=book 
            serializers=functionViewSerializers(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
        name=data.get("name")
        return Response(f"Successfully Books buy from username {name}")
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)