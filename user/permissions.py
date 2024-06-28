from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow Authenticated users to access the API.
    """

    def has_permission(self, request, view):
        """
        Check if the user is an admin.
        """
        return bool(request.user != 'AnonymousUser' and request.user.is_active == True)
    
class Admin(IsAuthenticated):
    """
    Custom permission to only allow admin users to access the API.
    """

    def has_permission(self, request, view):
        is_auth=super().has_permission(request,view)
        if is_auth:
            user=request.user.groups.using("default").all()
            if "Admin" in str(user):
                return True
        else:
            return False

class SuperAdmin(IsAuthenticated):
   """
    Custom permission to only allow Super admin users to access the API.
   """
   def has_permission(self, request, view):
        is_auth=super().has_permission(request,view)
        if is_auth:
            user=request.user.groups.using("default").all()
            if "Super Admin" in str(user):
                return True
        else:
            return False

class Users(IsAuthenticated):
   """
   Custom permission to only allow users to access the API.
   """
   def has_permission(self, request, view):
        is_auth=super().has_permission(request,view)
        if is_auth:
            user=request.user.groups.using("default").all()
            if "User" in str(user):
                return True
        else:
            return False
