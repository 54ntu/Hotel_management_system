from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsAdminOrReadOnly(BasePermission):
    #here i am creating custom permission class where only the admin is able to perform create operation
    def has_permission(self, request, view):
        if view.action in ['list','retrieve']:
            return True
        return request.user.is_superuser
    


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        # print(f"request we are getting is : {request.user.is_staff}") here admin is also a staff so it returns true for admin as well.
        if not request.user.is_staff:
            raise PermissionDenied(f"{request.user} is not a staff....Access denied...!!!")
        return request.user.is_staff