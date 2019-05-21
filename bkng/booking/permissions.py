from rest_framework import permissions
from rest_framework.permissions import BasePermission
from booking.models import User, MasterProfile


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsUserOwner(BasePermission):
    def has_permission(self, request, view):
        if 'pk' not in view.kwargs:
            return False
        profile = User.objects.get(pk=view.kwargs['pk'])
        if profile.user == request.user:
            return True

class IsUserHasMasterProfile(BasePermission):
    message = 'Вы уже являетесь мастером'
    def has_permission(self, request, view):
        try:
            profile = MasterProfile.objects.get(user=request.user)
            if profile:
                return False
        except MasterProfile.DoesNotExist:
            return True

