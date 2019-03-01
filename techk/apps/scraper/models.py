# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

"""
Category Model, it has:
    (PRIMARY_KEY, category name).
"""
class Category(models.Model):
    name = models.CharField(max_length=100)

"""
Model that describes Book class, is has:

    (PRIMARY_KEY, category(Foreign Key to Category table/model),
    title, book thumbnail, price, stock, description, UPC).

"""

class Book(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     title = models.CharField(max_length=100)
     thumbnail = models.URLField()
     price = models.PositiveIntegerField()
     stock = models.PositiveIntegerField()
     description=models.TextField()
     UPC=models.CharField(max_length=16,validators=[MinLengthValidator(16)])
