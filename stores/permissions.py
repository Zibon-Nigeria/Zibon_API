from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = "Unauthorized Access! Not The Owner"

    def has_object_permission(self, request, view, obj):
        if request.Method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner