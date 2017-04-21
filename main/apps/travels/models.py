from django.db import models
from apps.loginreg.models import Users
import datetime

class TripsManager(models.Manager):
    def addTrip(self, postData, user):
        #declare empty dictionary to hold errors
        errorList = {
            'errorsPresent': False,
            'destinationErrors': [],
            'descriptionErrors': [],
            'startDateErrors': [],
            'endDateErrors': []
        }
        #check if user attempted to submit any blanks or less than required length
        if len(postData['destination']) == 0:
            errorList['destinationErrors'].append("Destination cannot be blank!")
            errorList['errorsPresent'] = True
        if len(postData['description']) == 0:
            errorList['descriptionErrors'].append("Description cannot be blank!")
            errorList['errorsPresent'] = True
        if len(postData['start_date']) == 0:
            errorList['startDateErrors'].append("Start date cannot be blank!")
            errorList['errorsPresent'] = True
        if len(postData['end_date']) == 0:
            errorList['endDateErrors'].append("End date cannot be blank!")
            errorList['errorsPresent'] = True

        #check if user is attempting to enter date before today and whether end date is prior to start date
        if postData['start_date'] < str(datetime.date.today()):
            errorList['startDateErrors'].append("Start date cannot be before today! What are you even doing?")
            errorList['errorsPresent'] = True
        if postData['end_date'] < str(datetime.date.today()):
            errorList['endDateErrors'].append("End Date cannot be before today!")
            errorList['errorsPresent'] = True
        if postData['end_date'] < postData['start_date']:
            errorList['endDateErrors'].append("End Date cannot be before start date!")
            errorList['errorsPresent'] = True


        if errorList['errorsPresent']:
            return errorList
        else:
            self.create(destination = postData['destination'], description = postData['description'], start_date = postData['start_date'], end_date = postData['end_date'], plannedby_user_id = user)
            return errorList

# Create your models here.
class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    plannedby_user = models.ForeignKey(Users, related_name='planner')
    user_joining = models.ManyToManyField(Users, related_name='joining')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripsManager()