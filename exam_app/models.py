from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 9:
            errors["password"] = "Password should be at least 8 characters"    
        # test whether a field matches the email pattern
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address!"
        #password check
        if postData['password'] != postData['password_confirm']:
            errors['password'] = "The two password fields should match!"       
        return errors
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) == 0:
                errors["author"] = "Author is required"
        if len(postData['author']) < 4:
                errors["author"] = "Author More than 3 characters"
        if len(postData['desc']) < 11:
                errors["desc"] = "Description should be at least 11 characters"
        return errors
    
    def account_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
                errors["author"] = "First name is required"
        if len(postData['last_name']) == 0:
                errors["author"] = "Last name is required" 
        if len(postData['email']) == 0:
                errors["author"] = "email is required"              
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name= "quotes_uploaded", on_delete = models.CASCADE)
    desc = models.TextField(max_length=255)
    liked_quotes = models.ManyToManyField(User, related_name='users_who_like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = UserManager()   # Create your models here.
