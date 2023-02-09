from datetime import datetime

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from assessment.apps.manager.models import Status, Project, Task


class IsOwner(IsAuthenticated):
    """
    Permission that checks if the user is the owner of the object.
    Accessing either the Project.owner attribute or the Task.owner property
    so it works in either class.
    """

    def has_object_permission(self, request, view, obj):
        try:
            return obj.owner == request.user
        except AttributeError as e:
            return False


class IsPublic(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.is_public








class ObjectStatus(IsOwner):
    def has_object_permission(self, request, view, obj):
        self.message = {
            'details': f'the {obj.__class__.__name__} is: {obj.get_status_display()}.'}

        return obj.status == Status.IN_PROGRESS



class ProjectNotExpired(IsOwner):
    """
    Permission that checks if a Project Object is accessible or has expired.
    """

    def update_status(self, obj: Project):
        if obj.progress==100 :
            obj.status = Status.COMPLETED
            obj.save()
            return True
        return False
    def has_object_permission(self, request, view, obj: Project):
        self._is_owner = super().has_object_permission(request, view, obj)
        self.now = datetime.now().timestamp()

        self.project_expires_at = obj.due_date.timestamp()

        self.message = {'details': f'the {obj.__class__.__name__} has expired.',
                        'current_time': f"{self.now}",
                        'expired_since': f"{self.project_expires_at}"
                        }
        _expires_at = self.now < self.project_expires_at
        return self._is_owner and _expires_at

class TaskNotExpired(ProjectNotExpired):
    """
    Permission that checks if the object (and it's parent object)
    has expired.
    """

    def has_object_permission(self, request, view, obj: Task):

        _project_due_date = Project.objects.get(id=obj.project).due_date.timestamp()
        self.task_expires_at = obj.due_date.timestamp()


        self.message = {'details': f'the {obj.__class__.__name__} has expired.',
                        'current_time': f"{self.now}",
                        'expired_since': f"{self.task_expires_at}"
                        }

        return  self._is_owner and self.now < self.task_expires_at <self.project_expires_at


class ItemAvailable(IsOwner):
    """
    Permission that checks if the object is available for editing.
    Cheking the status of the object.
    Checking the due_date of the parent object.
    Checking the due_date of the object.
    Checking the progress of the project.
    """
    def has_object_permission(self, request, view, obj):
        self.message = {
            'details': f'the {obj.__class__.__name__} is: {obj.get_status_display()}.'}
        return obj.status == Status.IN_PROGRESS

