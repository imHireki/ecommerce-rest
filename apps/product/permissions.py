"""
Product app permissions
"""
from rest_framework import permissions


class ReadOnly(permissions.IsAdminUser):
    """ Perform an read only giving permissions just to safe methods"""
    
    def has_permission(self, request, view):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        return False
