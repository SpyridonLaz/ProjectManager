from datetime import datetime

from rest_framework.exceptions import ValidationError

from assessment.apps.manager.models import Status
from .models import Project, Task



class IsFutureDateValidator:
    """ 1
    Validates that a passed datetime object or string points to the future.
    """
    message = {'detail': 'Only a future datetime is accepted.',}
    def __init__(self, weeks=0,  days=0, hours=0, mins=0, seconds=0):

        self.gap =   weeks * 604800 + days * 86400 + hours * 3600 + mins * 60 + seconds
        self.now =  datetime.now().timestamp()


    def min_now(self, value,):
        # this method calcs the minimum time that is accepted as valid input.
        value_stamp = value.timestamp()
        if self.now >= value_stamp:
            raise ValidationError(detail=self.message)
        if self.gap and self.now + self.gap >= value_stamp:
            time_str = datetime.fromtimestamp(self.now + self.gap).isoformat()
            self.message['detail'] = 'Due date is too soon. Choose later than {gap}.'.format(gap=time_str)
            raise ValidationError(detail= self.message)

    def __call__(self, value):
        self.min_now(value)


class LessThanParentDueDateValidator:
    """
    This validator is used to ensure that the due_date of a **Task**
    is less than the due_date of it's parent Project.
    """
    message = {"details": "Task's due date cannot be greater than it's Project due date."}

    def __init__(self, instance:Task, parent):
        self.instance = instance
        self.parent = parent
        if instance.due_date > parent.due_date:
            raise ValidationError(detail=self.message)

class OutOfTimeRangeValidator(IsFutureDateValidator):
    """
    This validator is used to validate the due_date of a project or task.
    It ensures that the due_date is not less than the current time.
    It calculated the difference between the current time and the due_date
    and raises a ValidationError if the difference is less than 24 hours.
    Works in relation to a parent object(if given).
    """


    def __init__(self,  weeks=0, days=0, hours=0, mins=0, seconds=0):
        super().__init__( weeks=weeks, days=days, hours=hours, mins=mins, seconds=seconds)
        # earliest datetime in unix timestamp
        self.dt_min = int(self.now+ self.gap)
        # latest datetime in unix timestamp
        self.dt_max = None
        self.dT = None

    def __call__(self, value:datetime=None, instance=None,parent=None,):
        if parent:
            self.dt_max = parent.due_date.timestamp()

        self.instance = instance



        dT = value.timestamp()
        dt2 = self.instance.due_date.timestamp()
        if self.dt_min < dT < dt2:
            raise ValidationError(self.message)




class UniqueTitlePerProjectValidator:
    """
    Validates that a Task title is unique per project.
    """
    def __init__(self, title, project):
        project_id = project.id
        if Task.objects.filter(title=title, project=project_id).exists():
            raise ValidationError(
                detail={
                    'detail': 'Title must be unique per project.',
                    'invalid_field': title}
            )
