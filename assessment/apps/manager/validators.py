from datetime import datetime

from rest_framework.exceptions import ValidationError

from assessment.apps.manager.models import Status
from .models import Project, Task

class LockEdit:

    def get_project(self,obj):
        return obj.project


class EnsureFutureDateValidator:
    """ 1
    Validates that a passed date string points to the future.
    """

    def __init__(self, value):
        if datetime.now().timestamp() >= value.timestamp():
            raise ValidationError(
                {
                    'details': 'Only a future datetime is accepted.',
                    'invalid_field': value}
            )

############## COMPLETION ############################
class CompleteByExpirationValidator:
    """
    **update serializer**
    Object has expired if the current time is
     greater than the due_date
     """
    def __init__(self, instance=None):
        '''
        Comparison in Unix time to avoid naive/non-naive
        datetime comparison errors.
        '''
        value = instance.due_date
        current_time = datetime.now()
        if current_time.timestamp() > value.timestamp():
            instance.update_status(Status.EXPIRED)
            raise ValidationError(
                 {'details': f'the {instance.__class__.__name__} object has expired.',
                                 'current_time': datetime.now(),
                                 'expiry_date': value,
                                 })

class CompleteProjectOrTaskValidator:
    """
    2.1
"""
    def __init__(self, instance=None):
        self.instance = instance
        self.message = {'details': ['This project/task is  completed. Editing is not allowed']}
        self.max_int = 1
        self.min_int = 0


class CompleteByProgressValidator:
    """This class is used to validate the progress of a project or task.
        If the object's progress is set to 100% (represented by 1.0) then the task is
        completed and cannot be edited anymore.
    """
    message = {'details': ['Progress completed. Editing is not allowed. ']}

    def __init__(self, instance):
        self.instance = instance
        if instance == 1:
            instance.update_status(Status.COMPLETED)
            _query= Project.objects.get(id=instance.project_id)

            raise ValidationError(self.message)

class TaskOverdueValidator:
    """ 4
    for task models:
     Ensures that a given date is not later than the parent project due_date.
          """
    message = "out of time range"
    def __init__(self, project_obj):
        self.obj = project_obj

    def __call__(self, value):
        _project_date = self.obj.due_date
        if value.timestamp() > _project_date.timestamp():
            raise ValidationError({'details': 'Task object must have an earlier due date than it\'s parent Project',
                                      'max_accepted': _project_date,
                                   'given_value': value})

