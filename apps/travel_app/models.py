from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.db import models
import bcrypt
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email"
        if len(email) > 0:
            errors['email'] = "Email already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Insufficent password length"
        if postData['password'] != postData['cpassword']:
            errors['password'] = "Password doesn't match. Try again"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be longer than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be longer than 2 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password= models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    user = models.ForeignKey(User, related_name = "trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)