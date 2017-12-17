# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from datetime import datetime



import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile(r'^[a-zA-Z]{3,}$')
PSWD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])(?=.*[travels User!%*?&])[A-Za-z\d%*?&]{8,}$')
NUM_REGEX = re.compile(r'^\d{1,120}$')
DESC_REGEX =re.compile(r'^[a-zA-Z0-9 ]{15,}$')
FULL_NAME_REGEX = re.compile(r'^[A-Za-z]+\s[A-Za-z]+$')

import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "First name must be at least 3 character long and have only letters"
        if not NAME_REGEX.match(postData['last_name']):
            errors["last_name"] = "Last name must be at least 3 character long and have only letters"
        existing = User.objects.filter(email=postData['email'])
        if len(existing) > 0:
            errors["email"] = "Email is already in use"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email2"] = "email must be at least 4 characters long and look like: x@x.x"
        if (int(postData['birthday'][:4])<1900):
            errors['birthday'] = "I seriously doubt you were born before 1900. You don't look one day older than 1905"
        if not PSWD_REGEX.match(postData['password']):
            errors["password"] = "Password must include letters (capital and lower case, numbers and be at least 8 characters long)"
        if postData['password'] != postData['cpswd']:
            errors['cpsw'] = "passwrod and confirmation must match"
        return errors
    def register_user(self, postData):
        User_1=User.objects.create()
        User_1.first_name = postData['first_name']
        User_1.last_name = postData['last_name']
        User_1.email = postData['email']
        pswd = postData['password']
        User_1.password = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt(5))
        User_1.birthday = postData['birthday']
        User_1.save()
        return User_1
    def login_validator(self,postData):
        errors ={}
        u_list = User.objects.filter(email=postData['email'])
        if len(u_list) == 0:
            errors['login'] = "No user registered with that email"
            return [errors, u_list]
        User_1 = u_list[0]
        password = postData['password']
        password_db = User_1.password  
        if not bcrypt.checkpw(password.encode(), password_db.encode()):
            errors['login'] = "You have entered the wrong email and/or password combination"
        return [errors, User_1]



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length =255)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<\tfirst_name: {}\n \tlast_name: {}\n \temail_address: {}\n \tpassword:{}\n \tbirthday: {}\n \tcreated at: {}\n \tupdated at: {}\n>".format(self.first_name, self.last_name, self.email, self.password, self.birthday, self.created_at, self.updated_at)

    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData, creator_id):
        errors = {}
        if len(postData['destination'])==0:
            errors['destination'] = "Destination cannot be empty"
        if len(postData['plan'])==0:
            errors['plan'] = "Description cannot be empty"
        if len(postData["start_date"])==0 or len(postData["end_date"])==0:
            errors['date'] = "Dates cannot be empty!"
        print postData["start_date"]

        if postData['start_date'] > postData['end_date']:
            errors['trip_dates'] = "Start time must be before end time"

        now = datetime.now().strftime("%Y-%m-%d")
    
        if now > postData['start_date']:
            errors['trip_dates'] = "Must select a future date"
        
        if not len(errors)==0:
            return [errors, 0]

        creator = User.objects.get(id=creator_id)

        new_trip = Trip.objects.create(destination=postData['destination'], plan=postData['plan'], start_date=postData['start_date'], end_date=postData['end_date'], created_by=creator)
        return [errors, new_trip]



class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name="created_trips")
    users_joined = models.ManyToManyField(User, related_name="users_trips")
    objects= TripManager() 
    def  __repr__(self):
        return "<destination:{} start date:{} end date:{}>".format(self.destination,self.start_date, self.end_date)




"""
Let's say we have class players and team:
a tema has many players but a player has only one team -
to set the one-to-many relation between team and player do:

inside the class player (is the many class or if you preffer the class that is related to a unique object in the other class):

class Team(models.Model):
    etc...

class Players(models.Model):
    etc
    team = models.ForeignKey(Team, related_name="player")

**************************************************************

if the relation is many to many ie a player can play for many teams too:
the rerlation can be defiend in either class. Do only one of the following:

class Team(models.Model):
    etc...
    player = models.ManyToManyField(Players, related_name="team")

class Players(models.Model):
    etc
    team = models.ManyToManyField(Team, related_name="player


self join query:

        team=models.ManyToManyField("self", symetrical =False)
        team=models.OneToOneField("self", symetrical =False)




"""




