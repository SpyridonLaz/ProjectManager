from django.db import models

# Create your models here.






class User(models.Model):
    #/
    # build keycloak auth first
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name
