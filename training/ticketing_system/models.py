# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.


class User(models.Model):
    """ User Model. """

    email = models.CharField(max_length=150)
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.email


class Ticket(models.Model):
    """ Ticket Model. """

    STATUS = (
        ('O', 'open'),
        ('C', 'closed')
    )
    title = models.CharField(max_length=60)
    body = models.CharField(max_length=250)
    status = models.CharField(max_length=1, choices=STATUS, default='O')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ManyToManyField(User, related_name='assignee')
    created = models.DateField()

    def __str__(self):
        return self.title
