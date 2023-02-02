from django.db import models

from assessment.apps.projects.models import Project

# Create your models here.
'''
Provide a CRUD Task API. A task will contain a title, description, list of tags, parent project,
progress and finish date. The progress will be the completion percentage of the task
and will be updated manually from the project owner and when the task is
completed, it will not be editable. The tags will be user-defined strings that will be
used for the logical grouping of tasks under a project and will be passed optionally as
a query parameter on the task read operations.'''


class Task(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200 , null= False, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    progress = models.IntegerField()
    finish_date = models.DateField()

    def __str__(self):
        return self.title


class Tag(models.Model):

    tag = models.CharField(max_length=100)
    # ManyToMany instead of through model
    tasks = models.ManyToManyField(Task,related_name='tags')

    def __str__(self):
        return self.tag