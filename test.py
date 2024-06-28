data={"id":2,"name":"gk","group":"dd"}
data["group"]="kkkk"
print(data)


# from rest_framework.request import Request
# from rest_framework.views import APIView
# from ApiViewApp.serializers import ApiViewSerializers
# from SerializersApp.models import BookStore, Books
# from user.models import User
# from user.permissions import Admin, IsAuthenticated, Users
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import status
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from django.contrib.auth.models import Group
# from rest_framework.exceptions import PermissionDenied
# from user.Pagination import CustomPagination
# from rest_framework.decorators import api_view,authentication_classes,permission_classes


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def bookstore_detail(request, pk):
#     try:
#         user = request.user.id
        
#         # Check if user is admin or has permission to access user data
#         if Group.objects.filter(user=user, name="Admin").exists():
#             if not User.objects.filter(id=user).exists():
#                 raise PermissionDenied("You do not have permission to access this user's data")
            
#             # Query all BookStore objects excluding those belonging to Admin users
#             queryset = BookStore.objects.exclude(user__groups__name="Admin").values("id", "name", "user", "books", "Qty").order_by("id")
            
#             if not queryset:
#                 return Response("Data Not Found", status=status.HTTP_404_NOT_FOUND)
            
#             # Fetch related user and books information for each BookStore entry
#             for item in queryset:
#                 item["user"] = User.objects.filter(id=item["user"]).values("id", "first_name", "last_name", "email", "gender", "contact", "dob", "groups__name").first()
#                 item["books"] = Books.objects.filter(id=item["books"]).values("id", "name").first()
            
#             return Response(queryset, status=status.HTTP_200_OK)
#             # queryset = BookStore.objects.exclude(user__groups__name="Admin").prefetch_related(
#     #     Prefetch('user', queryset=User.objects.only('id', 'first_name', 'last_name', 'email', 'gender', 'contact', 'dob', 'groups__name'))
#     # ).prefetch_related(
#     #     Prefetch('books', queryset=Books.objects.only('id', 'name'))
#     # ).values("id", "name", "user", "books", "Qty").order_by("id")

#     # if not queryset:
#     #     return Response("Data Not Found")

#     # return Response(queryset, status=status.HTTP_200_OK)
#         # Handle case where user is an admin
#     except Exception as e:
#         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

