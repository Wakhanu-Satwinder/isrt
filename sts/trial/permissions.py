from rest_framework.permissions import BasePermission
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET','HEAD','OPTIONS'):
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_sataff
class IsOwner(BasePermission):
        def has_object_permission(self, request, view, obj):
             return obj.owner==request.user
        
        