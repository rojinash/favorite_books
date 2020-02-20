from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, post_data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(post_data['first_name'])<2:
            errors['first_name'] = 'Please enter a longer first name'
        if len(post_data['last_name'])<2:
            errors['last_name'] = 'Please enter a longer last name'
        if not EMAIL_REGEX.match(post_data['email']):           
            errors['email'] = "Invalid email address!"
        if len(post_data['password'])<8:
            errors['password'] = 'Please enter a longer password'
        if post_data['password']!= post_data['confirm_pw']:
            errors['confirm']='Your passwords do not match. Please try again'
        return errors

    def login_validator(self, post_data):
        errors={}
        current_user = User.objects.filter(email=post_data['email'])
        if len(current_user) < 1:
            errors['email'] = 'That email does not exist. Please register!'
        elif not bcrypt.checkpw(post_data['password'].encode(),current_user[0].password.encode()):
            errors['password'] = 'Wrong password. Try again!'
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name='uploaded_books', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
