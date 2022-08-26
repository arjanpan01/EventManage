from fnmatch import fnmatchcase
from unicodedata import name
from django.db import models

# Create your models here.
class AttendeeTable(models.Model):
    attendeeID = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=120)
    lName = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    attendance = models.BooleanField()

class AccompliceTable(models.Model):
    accompliceID = models.AutoField(primary_key=True)
    attendeeID = models.ForeignKey(AttendeeTable, on_delete=models.CASCADE)
    fName = models.CharField(max_length=120)
    lName = models.CharField(max_length=120)
    position = models.CharField(max_length=120)

class EmailTable(models.Model):
    emailID = models.AutoField(primary_key=True)
    attendeeID = models.ForeignKey(AttendeeTable, on_delete=models.CASCADE)
    email = models.EmailField()

class DateTable(models.Model):
    dateID = models.AutoField(primary_key=True)
    attendeeID = models.ForeignKey(AttendeeTable, on_delete=models.CASCADE)
    date = models.DateField()

class EventTable(models.Model):
    eventID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    startDate = models.DateField()
    endDate = models.DateField()
    location = models.CharField(max_length=120)

class CompanyTable(models.Model):
    companyID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    description = models.TextField()

class CompanyRepTable(models.Model):
    companyRepID = models.AutoField(primary_key=True)
    companyID = models.ForeignKey(CompanyTable, on_delete=models.CASCADE)
    fName = models.CharField(max_length=120)
    lName = models.CharField(max_length=120)
    email = models.EmailField()

class CompanyLinkTable(models.Model):
    companyLinkID = models.AutoField(primary_key=True)
    dateID = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    companyID = models.ForeignKey(CompanyTable, on_delete=models.CASCADE)
    eventID = models.ForeignKey(EventTable, on_delete=models.CASCADE)
    startTime = models.TimeField()
    endTime = models.TimeField()
    state = models.IntegerField()

class ProposeNewTimeTable(models.Model):
    proposeNewTimeID = models.AutoField(primary_key=True)
    companyLinkID = models.ForeignKey(CompanyLinkTable, on_delete=models.CASCADE)
    newStartTime = models.TimeField()
    newEndTime = models.TimeField()

class MessageTable(models.Model):
    messageID = models.AutoField(primary_key=True)
    proposeNewTimeID = models.ForeignKey(ProposeNewTimeTable, on_delete=models.CASCADE)
    messageText = models.TextField()

class BlockTimeTable(models.Model):
    blockTimeID = models.AutoField(primary_key=True)
    companyID = models.ForeignKey(CompanyTable, on_delete=models.CASCADE)
    eventID = models.ForeignKey(EventTable, on_delete=models.CASCADE)
    startTime = models.TimeField()
    endTime = models.TimeField()