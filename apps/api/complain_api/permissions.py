from rest_framework import permissions

class IsComplainantOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins full access
        if request.user.is_staff:
            return True
        # Restrict to complainant for other operations
        return obj.user == request.user