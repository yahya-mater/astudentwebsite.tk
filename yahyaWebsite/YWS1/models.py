from django.db import models

# Create your models here.

class workers(models.Model):
    name = models.CharField(max_length=64)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"ID : {self.id} name :{self.name} age : {self.age}"

class users(models.Model):
    user_name = models.CharField(max_length=64)
    user_gmail = models.CharField(max_length=64)
    user_password = models.CharField(max_length=64)

    def __str__(self):
        return f"ID : {self.id} name :{self.user_name} gmail : {self.user_gmail} password : {self.user_password}"

class orders(models.Model):
    user_gmail = models.CharField(max_length=64)
    user_order = models.CharField(max_length=64)
    user_order_date_month = models.PositiveSmallIntegerField(null=True)
    user_order_date_day = models.PositiveSmallIntegerField(null=True)
    user_order_date_hour = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return f"{self.id}-{self.user_order}-{self.user_gmail}-{self.user_order_date_month}/{self.user_order_date_day}"
