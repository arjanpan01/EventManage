from multiprocessing import Event
from tkinter import Widget
from django import forms
from .models import AttendeeTable, CompanyLinkTable, CompanyTable, EventTable, DateTable
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

    
class NewEventForm(forms.ModelForm):
    class Meta:
        model = EventTable
        fields = ('name', 'startDate', 'endDate', 'location')
        widgets = {
            'startDate': DateInput(),
            'endDate': DateInput(),
        }

class NewDateForm(forms.ModelForm):
    
    class Meta:
        model = DateTable
        fields = ('date',)
        widgets = {
            'date': DateInput(),
        }
    
class UpdateAttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendeeTable
        fields = ('fName','lName', 'position', 'attendance',)

class UpdateAccompliceForm(forms.ModelForm):
    class Meta:
        model = AttendeeTable
        fields = ('fName','lName', 'position',)

class AddStageForm(forms.ModelForm):

    def __init__(self, companyID, *args, **kwargs):
        super(AddStageForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelChoiceField(queryset=CompanyTable.objects.filter(companyID=companyID))
        #companies = forms.ModelChoiceField(queryset=CompanyTable.objects.filter(companyID=companyID))

        
    class Meta:
        model = CompanyLinkTable
        fields=('companyID', 'startTime', 'endTime', )
    