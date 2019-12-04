from rest_framework.permissions import IsAuthenticated, BasePermission


class OrderPermission(BasePermission):
    message = 'You must be logged in or the owner of the order to update/delete.'

    def has_permission(self, request, view):
        if view.action not in ['list', 'retrieve']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.customer
        return True


class CommentInOrderPermission(BasePermission):
    message = 'You must be logged in.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True


class PicturesInOrderPermission(BasePermission):
    message = 'You must be logged in and owner of the order.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return obj.customer == request.user
        return True


class CommentOrderPermission(BasePermission):
    message = 'You must be logged in or the owner of the comment to update/delete.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class PictureOrderPermission(BasePermission):
    message = 'You must be logged in or the owner of the order to update/delete.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.order.executor or request.user == obj.order.customer


class ReviewPermission(BasePermission):
    message = 'You must be logged in or the owner of the review to update/delete.'

    def has_permission(self, request, view):
        if view.action not in ['list', 'retrieve']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return request.user == obj.order.executor or request.user == obj.order.customer


class CommentsInReviewPermission(BasePermission):
    message = 'You must be logged in or the owner of the review to update/delete.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

class CommentReviewPermission(BasePermission):
    message = 'You must be logged in or the owner of the comment to update/delete.'

    def has_permission(self, request, view):
        if view.action != 'retrieve':
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action != 'retrieve':
            return request.user == obj.user or request.user == obj.user