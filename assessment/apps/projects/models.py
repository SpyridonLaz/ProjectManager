from django.db import models

# Create your models here.



class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name



'''Provide a CRUD Project API. A project will contain a title, description, progress and
finish date and will either be personal access (only the owner can view and edit it
and it’s tasks) or public (Any registered user will be able to view the project and it’s
tasks and only it’s owner will be able to edit it and it’s tasks). The progress will be
the completion percentage of the tasks of the project and will be automatically
updated (Using any calculation algorithm of your choice).'''

class Project(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200 , null= False, blank=True)
    progress = models.IntegerField()
    finish_date = models.DateField()
    is_public = models.BooleanField()

    def __str__(self):
        return self.title
