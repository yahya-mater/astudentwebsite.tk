from django.db import models

# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    authorised = models.BooleanField()

    def __str__(self):
        return f"ID : {self.id} \nname :{self.name} \ngmail : {self.gmail} \npassword : {self.password} \nauthorised : {self.authorised}"
