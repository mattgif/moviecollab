from django.db import models

# class Person(models.Model):
#     id = models.IntegerField(unique=True, primary_key=True)
#     name = models.CharField(max_length=128)
#     image = models.URLField(max_length=512)
#     projects = models.ManyToManyField(Project)
#
#     def __str__(self):
#         return self.name
#
# class Project(models.Model):
#     id = models.IntegerField(unique=True, primary_key=True)
#     title = models.Charfield(max_length=128)
#
#     def __str__(self):
#         return self.title
