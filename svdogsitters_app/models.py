from django.db import models
import re
import datetime

class UsersManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters"
        if not email_regex.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['phone']) != 10:
            errors['phone'] = "Phone number must have 10 numbers"
        if len(postData['password']) < 8:
            errors['password'] = "Password must have at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match"
        
        return errors

class DogsManager(models.Manager):
    def dog_registration_validator(self, postData):
        errors = {}

        if datetime.datetime.strptime(postData['dog_birthday'], '%Y-%m-%d') > datetime.datetime.now():
            errors['dog_birthday'] = "Birthday should be in the past" 
        if len(postData['dog_breed']) < 3:
            errors['dog_breed'] = "Dog breed must have at least 3 characters"
        if len(postData['vet_clinic']) < 5:
            errors['vet_clinic'] = "Vet clinic must have at least 5 characters"
        if len(postData['vet_address']) < 8:
            errors['vet_address'] = "Vet address must have at least 8 characters"
        if len(postData['vet_phone']) != 10:
            errors['vet_phone'] = "Vet phone must have 10 numbers"
        
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Dogs(models.Model):
    owner = models.ForeignKey(Users, related_name='owner_dog', on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=255)
    dog_birthday = models.DateField()
    dog_breed = models.CharField(max_length=255)
    dog_weight = models.CharField(max_length=255)
    vet_clinic = models.CharField(max_length=255)
    vet_address = models.CharField(max_length=255)
    vet_phone = models.CharField(max_length=10)
    dog_allergies = models.TextField()
    dog_comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DogsManager()

class Requests(models.Model):
    requester = models.ForeignKey(Users, related_name='requester_service', on_delete=models.CASCADE)
    service = models.CharField(max_length=255)
    estimate = models.IntegerField()
    status = models.CharField(max_length=255, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 