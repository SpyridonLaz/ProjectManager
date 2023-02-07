from abc import ABC
from datetime import datetime

from rest_framework.exceptions import ValidationError

from assessment.apps.manager.models import Status
from .models import Project, Task



class EnsureFutureDateValidator(ABC):
    """ 1
    Validates that a passed datetime object or string points to the future.
    """

    def __init__(self,value:datetime or int, min_time=None):
        value = value.timestamp() if isinstance(value, datetime) else value
        now = min_time or  datetime.now().timestamp()
        if now >= value.timestamp():
            raise ValidationError(
                {
                    'details': 'Only a future datetime is accepted.',
                    'invalid_field': value}
            )




















############## COMPLETION ############################
class CompleteByExpirationValidator(EnsureFutureDateValidator):
    """
     Object has expired if the current time is
      greater than the due_date

         Comparison in Unix time to avoid naive/non-naive
         datetime comparison errors.
         """
    def __init__(self, value, message=None, time=None, instance=None):
        super().__init__(value)

        self.message = message or {'details':  f'the {instance.__class__.__name__} object has expired.',
                     'current_time': datetime.now(),
                     'expired': instance.due_date,
                     }



        current_time = time or datetime.now()
        if current_time.timestamp() > instance.due_date.timestamp():
            if instance.status == Status.IN_PROGRESS:
                instance.update_status(Status.EXPIRED)
                raise ValidationError(self.message)


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



class OutOfTimeRangeValidator(EnsureFutureDateValidator):
    """
    This validator is used to validate the due_date of a project or task.
    It ensures that the due_date is not less than the current time.
    It calculated the difference between the current time and the due_date
    and raises a ValidationError if the difference is less than 24 hours.
    """
    message = {'details': 'Due date must be at least 12 hours from now '}


    def __init__(self, value, time=None, days=0, hours=0, mins=0, seconds=0):
        self.gap= time or days*24*60*60 + hours*60*60 + mins*60 + seconds
        self.dt_min = int(datetime.now().timestamp()+ self.gap)

        super().__init__(value=self.dt_min)

        # minimum time in unix


    def __call__(self, value:datetime=None, instance=None,parent=None,):

        if value.timestamp() < self.dt_min:
            raise ValidationError(self.message)
        self.instance = instance
        if parent:
            self.dt_max = parent.due_date.timestamp()
            if not self.dt_min > self.dt_max:
                raise ValidationError(self.message)



        dT = value.timestamp()
        dt2 = self.instance.due_date.timestamp()
        if self.dt_min < dT < dt2:
            raise ValidationError(self.message)


