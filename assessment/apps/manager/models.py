from django.contrib.auth.models import User,Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


#from assessment.apps.users.models import User
# Create your models here.








class Status(models.TextChoices):

    IN_PROGRESS = "1", "In Progress"
    CANCELED = "2", "Canceled"
    COMPLETED = "3", "Completed"
    INCOMPLETE = "4", "Incomplete"



class Project(models.Model):
    '''A project will contain a title, description, progress and
    finish date and will either be personal access (only the owner can view and edit it
    and it’s tasks) or public (Any registered user will be able to view the project and it’s
    tasks and only it’s owner will be able to edit it and it’s tasks).

    The progress will be
    the completion percentage of the tasks of the project and will be automatically
    updated.

    We assume that a valid due_date is more than 1 day from the current date and that
    the progress will be the completion percentage of the tasks of the project and will be
    automatically updated.
    '''

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=200 ,
                                   null= False,
                                   blank=True)
    progress =    models.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      default=0,
                                      )
    due_date = models.DateTimeField()
    status = models.SmallIntegerField(choices=Status.choices, default=Status.IN_PROGRESS )
    is_public = models.BooleanField(default=False)


    def __str__(self):
        return self.title






class Task(models.Model):
    """

    A task contains a title, description, list of tags, parent project,
    progress and finish date. The progress will be the completion percentage of the task
    and will be updated manually from the project owner and <<<when the task is
    completed, it will not be editable>>>. The tags will be user-defined strings that will be
    used for the logical grouping of tasks under a project and will be passed optionally as
    a query parameter on the task read operations.
    a task is completed when progress == 100 OR when
    """
    title = models.CharField(max_length=200, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=200 ,
                                   blank=True)
    progress =    models.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      default=0,
                                      )

    # if progress == 100, task is completed
    # new progress value > previous progress value
    status = models.CharField(max_length=20,
                              choices=Status.choices ,
                              default=Status.IN_PROGRESS)
    #todo add validation for 0-100
    due_date = models.DateTimeField() #todo not later than project end date
    tag = models.CharField(max_length=50,
                           blank=True)


