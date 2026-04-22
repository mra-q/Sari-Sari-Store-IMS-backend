# Inventory-backend/apps/users/permissions.py

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permission class to allow only users with 'owner' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'owner'
