"""Module with all models that correspond to data base tables """

from django.db import models


class User(models.Model):
    """User model"""
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=250)

    class Meta:
        ordering = ('id',)


class Post(models.Model):
    """Post model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    content = models.CharField(max_length=9000)
    likes = models.CharField(max_length=9000)
    created_date = models.DateField(auto_now=False, auto_now_add=True)


    class Meta:
        ordering = ('id',)