from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import sys
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

 
class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        
        try:
            name = postData['name']
            alias = postData['alias']
            email = postData['email'].lower()
            password = postData['password']
            cpassword = postData['cpassword']
            birth_date = postData['birth_date']

            if len(name) < 4:
                errors['inName'] = 'Name is too short; minimum 4 characters are required!'

            if len(alias) < 2: 
                errors['inAlias'] = 'Alias is too short; minimum 2 characters are required!'

            if len(email) < 1: 
                errors['inEmLength'] = 'Email is required!'
            elif not EMAIL_REGEX.match(email):
                errors['inEmail'] = 'Invalid email address!' 
            
            if len(password) < 8:
                errors['inPassword'] = "Pasword must be minimum 8 characters long!"  
            elif password != cpassword:
                errors['inCPassword'] = 'Passwords do not match!'    

            if len(birth_date) < 1: 
                errors['inBDate'] = 'Date of birth is required!'    

            if not errors:  
                if User.objects.filter(email=email).exists():
                    errors['user_found'] = 'User already exists'
                else:
                    # if no errors and new user, add user to the database
     
                    hashpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

                    user = User()
                    user.name = name
                    user.alias = alias
                    user.email = email
                    user.password = hashpass
                    user.birth_date = birth_date
                    user.save()

                    return user

        except:
            print sys.exc_info()
            errors['userInput'] = 'An error has occured. Please fill the form again.'

        return errors    

    def validate_login(self, postData):
        errors = {}

        try:
            email = postData['email']
            password = postData['password']

            crt_user=User.objects.filter(email=email)
            if len(crt_user) == 1: # because crt_user is a list with 1 element 
                hashpassdb = crt_user[0].password
                print "hashpassdb:", hashpassdb
                if bcrypt.checkpw(password.encode(), hashpassdb.encode()):
                    return crt_user[0]
                else:
                    error['login'] = 'Email or password not valid '
                
            else:
                error['emailInp'] = 'Wrong email or password'
        
        except: 
            errors['userInput'] = 'An error has occured. Please try again.'
        
        return errors        
            


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    poked_users = models.ManyToManyField("self", related_name="pokers", symmetrical=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    poke_count = models.IntegerField(default=0)
    objects = UserManager()         
    def __str__(self):
        return self.name
         