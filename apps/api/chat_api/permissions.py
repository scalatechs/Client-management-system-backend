from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.client, obj.representative]

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'

class IsRepresentative(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'customer representative'