# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



# postdata = dictionary
class UserManager(models.Manager):
    def register(self, postdata):
        errors = []
        if len(postdata['username']) < 1:
            errors.append("Please enter a User Name")

        try:
            username_check = User.objects.get(username= postdata['username'])
            if len(username_check) > 0:
                errors.append("Username is taken")
        except:
            pass
        # checks if the first name is present
        if(len(postdata['first_name']) < 1):
            errors.append('Please Enter a First Name')
        
        # checks if the last name is present
        if(len(postdata['last_name']) < 1):
            errors.append('Please Enter a Last Name')
    
        # checks if a birthday has been entered
        if (len(postdata['birthday']) > 1):
            age_verification = datetime.today() - relativedelta(years=18)
            birthday = datetime.strptime(postdata['birthday'], '%Y-%m-%d')
            # checks if there person is atleast 18 years old 
            if age_verification < birthday:
                errors.append("You Must be 18")

        #checks if a birthday was not entered
        if (len(postdata['birthday']) < 1):
            errors.append("Please enter a Birthday")


        if (len(postdata['password']) < 8):
            errors.append('Password is too short')

        # checks if the email is present
        if(len(postdata['email']) < 1):
            errors.append('Please Enter a Email')

        # checks the email present
        if(len(postdata['password']) < 1):
            errors.append('Please Enter a Password')

        # checks that both the password and password confirmation are the same
        if(postdata['password'] != postdata['password_confirmation']):
            errors.append('Passwords Do not Match')

        # checks if the email already exists
        try:
            User.objects.get(email = postdata['email'])
            errors.append('Email already Exists')
        except:
            pass
        try:
            validate_email(postdata['email'])
        except ValidationError as e:
            errors.append("Email must be in a valid format")


        # return errors and cancel the user creation
        if errors:
            return {'error_msg': errors}

            # if no errors create the user
        else:
            hashedpassword =  bcrypt.hashpw(postdata['password'].encode(), bcrypt.gensalt())
            
            new_user = User.objects.create(
            username = postdata['username'],
            first_name = postdata['first_name'],
            last_name = postdata['last_name'],
            birthday = postdata['birthday'],
            email = postdata['email'],
            password = hashedpassword,
            )
            success = ["Thank you {}, your account has been created".format(new_user.first_name)]
            return {'new_user': new_user, 'success': success}
      

    # postdata = dictionary
    def login(self, postdata):
        try:
            database_user = User.objects.get(username = postdata['username'])
            if bcrypt.checkpw(postdata['password'].encode(), database_user.password.encode()):
                return {'logged_user': database_user}
            else:
                return {'error_msg': ['Username and Password combination is invalid']}
        except:
            return {'error_msg': ["Username and Password combination is invalid"]}

    def edit(self, postdata, user_id):
        errors = []
        user = User.objects.get(id = user_id)
        if bcrypt.checkpw(postdata['password_check'].encode(), user.password.encode()):
            # Do nothing if the field has nothing in it
            if len(postdata['first_name']) > 1:

                user.first_name = postdata['first_name']
                user.save()
            if len(postdata['last_name']) > 1:
                user.last_name = postdata['last_name']
                user.save()
            
            # check the email 
            if len(postdata['email']) > 1: 
                try:
                    User.objects.get(email = postdata['email'])
                    errors.append('That email is already taken')
                except:
                    try:
                        validate_email(postdata['email'])
                        user.email = postdata['email']
                        user.save()
                    except ValidationError as e:
                        errors.append("Email must be in a valid format")

            # check the passsword
            if len(postdata['new_password']) > 1:
                    if postdata['new_password'] == postdata['password_confirmation']:
                        user.password = bcrypt.hashpw(postdata['new_password'].encode(), bcrypt.gensalt())
                    else:
                        errors.append("New Password does not match confirmation")

            if errors:
                return {'error_messages': errors}
            
            else:
                return {'success': ["Account Information Updated"]}
        else:
            errors.append("Incorrect Password")
            return {'error_messages': errors}
            
            
    
        




class User(models.Model):
    username = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    birthday = models.DateField()
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
        

