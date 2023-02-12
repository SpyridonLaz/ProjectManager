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




class ProjectStatus(IsOwner):
    _message = {'details': "finished."}
    def has_object_permission(self, request, view, obj):
        if obj.status == Status.IN_PROGRESS:
            return True
        else:
            self.message = obj
            return False
    @property
    def message(self):
        return  self._message
    @message.setter
    def message(self, obj):
        self._message['details']= f'{obj.__class__.__name__} is: {obj.get_status_display()}.'

class TaskStatus(ProjectStatus):
    def has_object_permission(self, request, view, obj):

        return super().has_object_permission(request, view, obj.project)\
            and super().has_object_permission(request, view, obj)


class ProjectNotExpired(IsOwner):
    """
    Permission that checks if a Project Object is accessible or has expired.
    """
    now = datetime.now()
    message = {'details': 'expired.' }
    def has_object_permission(self, request, view, obj):
        self.expires_at = obj.due_date
        if self.now.timestamp() <= self.expires_at.timestamp():
            return True
        else:
            self.get_message(obj, self.now, self.expires_at)
            return  False

    def get_message(self,obj,now,expired_since):
        self.message['details'] = '{} expired.'.format(obj.__class__.__name__)
        self.message['current_time'] = now
        self.message['expired_since'] = expired_since

class TaskNotExpired(ProjectNotExpired):
    """
    Permission that checks if the object (and it's parent object)
    has expired.
    """
    def has_object_permission(self, request, view, obj: Task):
        project_expires =   super().has_object_permission(request, view, obj.project)
        task_expires = super().has_object_permission(request, view, obj)
        print("PERMIT STATUS: ", project_expires and task_expires)

        return project_expires and task_expires
