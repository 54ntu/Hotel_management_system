from rest_framework.permissions import BasePermission



class IsAdminOrReadOnly(BasePermission):
    #here i am creating custom permission class where only the admin is able to perform create operation
    def has_permission(self, request, view):
        if view.action in ['list','retrieve']:
            return True
        return request.user.is_superuser