from rest_framework.permissions import IsAuthenticated, BasePermission
from users.models import MainUser

class UniPermission(BasePermission):
    message = 'You must be the admin.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action is not 'list':
            return request.user.is_superuser