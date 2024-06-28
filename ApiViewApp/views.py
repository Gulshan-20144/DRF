from rest_framework.request import Request
from rest_framework.views import APIView
from ApiViewApp.serializers import ApiViewSerializers
from SerializersApp.models import BookStore, Books
from user.models import User
from user.permissions import Admin, IsAuthenticated, Users
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from user.Pagination import CustomPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class UploadDataView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    serializer_class=ApiViewSerializers
    paginations_class=CustomPagination
    http_method_names=["get","put","post","delete","patch"]
    def get_permissions(self):
        permission_mapping={
            "post":[Admin],
            "get":[Admin|Users],
            "patch":[Admin | Users]
        }
        permission=[permission() for permission in permission_mapping.get(self.request.method.lower(),[])]
        return permission
    @swagger_auto_schema(request_body=ApiViewSerializers)
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
            queryset = BookStore.objects.using("default").all().exclude(user__groups__name="Admin").values("id","name", "user", "books", "Qty").order_by("id")
            if not queryset:
                return Response("Data Not Found")
            search_query = request.query_params.get('search', None)
            if search_query:
                queryset = queryset.filter(name__icontains=search_query) | queryset.filter(user__first_name__icontains=search_query)

            for lists in queryset:
                lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
                lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request, self)
            return paginator.get_paginated_response(paginated_queryset)
        else:
            if not Group.objects.using("default").filter(user=user,name="Admin").exists():
                if not BookStore.objects.using("default").filter(id=kwargs.get("pk"),user=user).exists():
                    raise PermissionDenied("you have not permission to access this user data")
            queryset = BookStore.objects.using("default").filter(id=kwargs.get("pk")).values("id","name", "user", "books", "Qty")
            if not queryset:
                return Response("Data Not Found")
            
            for lists in queryset:
                lists["user"]=User.objects.using("default").filter(id=lists["user"]).values("id","first_name","last_name","email","gender","contact","dob","groups__name")
                lists["books"]=Books.objects.using("default").filter(id=lists["books"]).values("id","name")
            return Response(queryset,status=status.HTTP_200_OK)
        
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
    
    def delete(self ,request,*args,**kwargs):
        try:
            instance=BookStore.objects.using("default").filter(id=kwargs.get("pk")).first()
            if instance:
                instance.delete()
                return Response("Data delete Succesfully",status=status.HTTP_204_NO_CONTENT)
            raise Exception("Data already delete Succesfully")
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)