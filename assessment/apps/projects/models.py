from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


#from assessment.apps.users.models import User
# Create your models here.





'''Provide a CRUD Project API. A project will contain a title, description, progress and
finish date and will either be personal access (only the owner can view and edit it
and it’s tasks) or public (Any registered user will be able to view the project and it’s
tasks and only it’s owner will be able to edit it and it’s tasks). The progress will be
the completion percentage of the tasks of the project and will be automatically
updated (Using any calculation algorithm of your choice).'''


class Status(models.TextChoices):

    IN_PROGRESS = "1", "In Progress"
    CANCELED = "2", "Canceled"
    COMPLETED = "3", "Completed"
    INCOMPLETE = "4", "Incomplete"


class Project(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200 ,
                                   null= False,
                                   blank=True)
    progress =    models.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      default=0,
                                      )

    finish_date = models.DateTimeField()
    status = models.SmallIntegerField(choices=Status.choices, default=Status.IN_PROGRESS)
    is_public = models.BooleanField(default=False)


    def __str__(self):
        return self.title
