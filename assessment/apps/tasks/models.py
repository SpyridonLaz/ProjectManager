from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from assessment.apps.projects.models import Project, Status


# Create your models here.




class Tag(models.Model):
    """
    A tag is a string that will be used for the logical grouping
     of tasks under a project and will be passed <<<optionally>>>
     as a query parameter on the task read operations.
    """
    tag = models.CharField(unique=True, max_length=50)
    tasks = models.ManyToManyField('Task', related_name='tags')

class Task(models.Model):
    """

    A task contains a title, description, list of tags, parent project,
    progress and finish date. The progress will be the completion percentage of the task
    and will be updated manually from the project owner and <<<when the task is
    completed, it will not be editable>>>. The tags will be user-defined strings that will be
    used for the logical grouping of tasks under a project and will be passed optionally as
    a query parameter on the task read operations.

    """
    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=200 ,
                                   null= False,
                                   blank=True)
    progress =    models.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      default=0,
                                      )

    # if progress == 100, task is finished
    # new progress value > previous progress value
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    #todo add validation for 0-100
    finish_date = models.DateTimeField() #todo not later than project end date
    finished = models.BooleanField(default=False )

    def __str__(self):
        return self.title



