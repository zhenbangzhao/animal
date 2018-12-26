from django.db import models


class pet(models.Model):

    petName = models.CharField(max_length=10)
    petId = models.CharField(max_length=4)
    gender = models.CharField(max_length=10)
    year = models.IntegerField()
    kind = models.CharField(max_length=10)


class UserModel(models.Model):
    userName = models.CharField(max_length=10)
    password = models.CharField(max_length=10)