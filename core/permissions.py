from rest_framework.permissions import BasePermission

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_freelancer

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client