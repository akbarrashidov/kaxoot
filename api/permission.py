from rest_framework.permissions import BasePermission

class IsRoomOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.admin == request.user
