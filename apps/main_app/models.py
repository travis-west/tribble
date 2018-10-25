from __future__ import unicode_literals
from django.db import models

from apps.users_app.models import User


class JobManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        ### TITLE VALIDATION ###
        if len(postData['title']) == 0:
            errors["title"] = "Title must be entered"
        elif len(postData['title']) < 3:
            errors["title"] = "Title must be at least 3 characters"
        elif len(postData['title']) > 254:
            errors["title"] = "Woah there! That's a really long title"

        ### DESCRIPTION VALIDATION ###
        if len(postData['description']) == 0:
            errors["description"] = "Description must be entered"
        elif len(postData['description']) < 3:
            errors["description"] = "Description must be at least 3 characters"
        elif len(postData['description']) > 254:
            errors["description"] = "Woah there, greedy! That's a really long description"

        ### LOCATION VALIDATION ###
        if len(postData['location']) == 0:
            errors["location"] = "Location must be entered"
        elif len(postData['location']) < 3:
            errors["location"] = "Location must be at least 3 characters"
        elif len(postData['location']) > 254:
            errors["location"] = "Woah there, greedy! That's a really long location"

        return errors

class Job(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name = "owns")
    assigned_to = models.ForeignKey(User, related_name = "has_jobs", null="True")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = JobManager()
    def __repr__(self):         
        return "<Job object: {} {}>".format(self.id, self.title)





class CategoryManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        ### TITLE VALIDATION ###
        if len(postData['newcategory']) == 0:
            errors["newcategory"] = "Category name must be entered"
        elif len(postData['newcategory']) < 3:
            errors["newcategory"] = "Category name must be at least 3 characters"
        elif len(postData['newcategory']) > 254:
            errors["newcategory"] = "Woah there! That's a really long category name"

        return errors


class Category(models.Model):
    category_name = models.CharField(max_length=250)
    has_job = models.ManyToManyField(Job, related_name = "has_category")
    objects = CategoryManager()
    def __repr__(self):         
        return "<Category object: {} {}>".format(self.id, self.title)
    