from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#UserManager
class UserManager(models.Manager):
    def register(self, postData):
        #declare empty dictionary to hold errors
        errorList = {
            'errorsPresent': False,
            'emailErrors': [],
            'fnameErrors': [],
            'lnameErrors': [],
            'pwordErrors': [],
            'confpwErrors': [],
            'emailInDb': [],
        }
        #check if user attempted to submit any blanks or less than required length
        if len(postData['email']) == 0:
            errorList['emailErrors'].append("Email cannot be blank!")
            errorList['errorsPresent'] = True
        if len(postData['fname']) < 3:
            errorList['fnameErrors'].append("First name must be at least 3 characters!")
            errorList['errorsPresent'] = True
        if len(postData['lname']) < 3:
            errorList['lnameErrors'].append("Last name must be at least 3 characters!")
            errorList['errorsPresent'] = True
        if len(postData['pword']) < 8:
            errorList['pwordErrors'].append("Password must be at least 8 characters!")
            errorList['errorsPresent'] = True

        #vcheck if email exists in database and catch DoesNotExist error if it doesnt
        try:
            preExist = self.get(email = postData['email'])
        except self.model.DoesNotExist:
            preExist = False

        #if entry exists, preExist will not be false, append error, else continue validations for email
        if preExist is False:
            #check if first name is alpha
            if not postData['fname'].isalpha():
                errorList['fnameErrors'].append("First name must be all letters!")
                errorList['errorsPresent'] = True
            if not postData['lname'].isalpha():
                errorList['lnameErrors'].append("Last name must be all letters!")
                errorList['errorsPresent'] = True
            if not EMAIL_REGEX.match(postData['email']):
                errorList['emailErrors'].append("Email improperly formatted!")
                errorList['errorsPresent'] = True
            if not postData['pword'] == postData['confpw']:
                errorList['confpwErrors'].append("Passwords must match!!")
                errorList['errorsPresent'] = True
        else:
            errorList['emailInDb'].append("Email already in DB!")
            errorList['errorsPresent'] = True
            
        if errorList['errorsPresent']:
            return errorList    
        else:
            #create entry and return no errors
            self.create(first_name = postData['fname'], last_name = postData['lname'], email = postData['email'], password = postData['pword'])

            return errorList
    
    def login(self, postData):
        #declare empty dictionary to hold errors
        errorList = {
            'errorsPresentLogin': False,
            'emailLoginErrors': [],
            'pwordLoginErrors': [],
        }

        #check if email or password is empty
        if len(postData['email_login']) == 0:
            errorList['emailLoginErrors'].append("Email can't be blank!")
            errorList['errorsPresentLogin'] = True
        if len(postData['pword_login']) == 0:
            errorList['pwordLoginErrors'].append("Password can't be blank!")
            errorList['errorsPresentLogin'] = True

        #check if errors are present
        if errorList['errorsPresentLogin']:
            return errorList
        
        #compare email against db capture doesnotexist error
        try:
            preExist = self.get(email = postData['email_login'])
        except self.model.DoesNotExist:
            errorList['emailLoginErrors'].append("Email does not exist!")
            errorList['errorsPresentLogin'] = True
            return errorList

        if not postData['email_login'] == preExist.email:
            errorList.append("Sorry, email does not exist or match our database")
            errorList['errorsPresentLogin'] = True
        if not postData['pword_login'] == preExist.password:
            errorList['pwordLoginErrors'].append("Sorry, wrong password")
            errorList['errorsPresentLogin'] = True

        return errorList
# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #connect instance of UserManager
    objects = UserManager()
