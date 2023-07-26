from rest_framework import permissions

class IsStoreOwner(permissions.BasePermission):
    message = "Unauthorized Access! You Are Not The Owner Of This Store"

    def has_object_permission(self, request, view, obj):
        if request.Method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner