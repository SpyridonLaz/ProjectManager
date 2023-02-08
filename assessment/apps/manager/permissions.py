from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from assessment.apps.manager.models import Status


class IsProjectOwner(IsAuthenticated):
    """
    Permission that checks if the user is the owner of the object.
    Accessing either the Project.owner attribute or the Task.owner property
    so it works in either class.
    """

    def has_object_permission(self, request, view, obj):
        try:
            return obj.owner == request.user
        except AttributeError as e:
            print(e)
            return False


class IsPublic(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.is_public


class ObjectStatus(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.message = {
            'details': f'the {obj.__class__.__name__} is: {obj.get_status_display()}.'}
        if obj.__class__.__name__ == 'Project':

            return obj.status == Status.IN_PROGRESS
        return obj.status == Status.IN_PROGRESS

