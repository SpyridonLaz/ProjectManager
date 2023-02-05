from datetime import datetime

from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



# from assessment.apps.users.models import User
# Create your models here.


class Status(models.IntegerChoices):

    IN_PROGRESS = 1, _("In Progress") # on time scheule
    CANCELED = 2, _("Canceled")  # canceled by owner
    COMPLETED =  3, _("Completed") # completed tasks
    EXPIRED = 4, _("Expired") # incompleted tasks


class Project(models.Model):
    '''A project will contain a title, description, progress and
    finish date and will either be personal access (only the owner can view and edit it
    and it’s tasks) or public (Any registered user will be able to view the project and it’s
    tasks and only it’s owner will be able to edit it and it’s tasks).

    The progress will be
    the completion percentage of the tasks of the project and will be automatically
    updated.

    We assume that a valid due_date value is >=24 hours later from the current date and that
    the progress will be the completion percentage of the tasks of the project and will be
    automatically updated.
    '''

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=400,
                                   null=False,
                                   blank=True)
    progress = models.DecimalField(max_digits=3,
                                   decimal_places=2,
                                   default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(1)]
                                   )
    due_date = models.DateTimeField(null=False,
                                    default=(timezone.now() + timezone.timedelta(hours=24)),

                                    )
    status = models.PositiveSmallIntegerField( choices=Status.choices,
                                               default=Status.IN_PROGRESS)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    '''A tag will contain a name and will be used to group tasks project wide/global wide

    '''
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """

    A task contains a title, description, list of tags, parent project,
    progress and finish date. The progress will be the completion percentage
    of the task and will be updated manually from the project owner and <<<when the task is
    completed, it will not be editable>>>. The tags will be user-defined strings that will be
    used for the logical grouping of tasks under a project and will be passed optionally as
    a query parameter on the task read operations.
    a task is completed when progress == 100 OR when
    """
    title = models.CharField(max_length=200,
                             unique=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)
    description = models.CharField(max_length=200,
                                   blank=True)

    progress = models.DecimalField(max_digits=3,
                                   decimal_places=2,
                                   default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(1)]
                                   )

    # check status model for choices
    # and conditions
    status = models.PositiveSmallIntegerField(choices=Status.choices,
                                              default=Status.IN_PROGRESS)
    due_date = models.DateTimeField(null=False     )
    tags = models.ManyToManyField(Tag,related_name='tasks')

    def __str__(self):
        return self.title

    @property
    def owner(self):
        """
        Convenient property to use in permissions
        interchangeably with the owner attribute of
        the parent Project!
        """
        return self.project.owner

    @property
    def is_public(self):
        """
        Convenient property to use in permissions
        interchangeably with the is_public attribute of
        the parent Project!
        """
        return self.project.is_public
