
from rest_framework.permissions import IsAuthenticated

class IsOwner( IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user



class IsVisible(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.is_public








