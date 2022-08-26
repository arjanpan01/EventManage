from multiprocessing import Event
from sqlite3 import Date
from django.shortcuts import render, redirect
from .models import EventTable, CompanyLinkTable, DateTable, AttendeeTable, CompanyTable, AccompliceTable, EmailTable
from .forms import AddStageForm, NewEventForm, NewDateForm, UpdateAttendanceForm, UpdateAccompliceForm
from django.core import serializers
from django.http import HttpResponseRedirect
from datetime import datetime
import re

def initialTable(request):
    events = EventTable.objects.all()
    return render(request, 'events.html', {"events": events})

def newEvent(request):
    if request.method == "POST": 
        eventForm = NewEventForm(request.POST)
        if eventForm.is_valid():
            eventForm.save()
            return redirect('/')
    eventForm = NewEventForm()
    return render(request, 'newEvent.html', {"eventForm": eventForm})


def updateEvent(request, eventID):
    event = EventTable.objects.get(pk=eventID)
    eventForm = NewEventForm(request.POST or None, instance = event)
    if eventForm.is_valid():
        eventForm.save()
        return redirect('initialTable')

    return render(request, 'updateEvent.html', {"event": event, "form": eventForm})

def goToDashboard(request, eventID):
    times = list(range(9,18))
    event = EventTable.objects.get(pk=eventID)
    companyLinkTable = CompanyLinkTable.objects.filter(eventID=eventID)

    if request.method == "POST":
        selectDate = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    else:
        selectDate = event.startDate
    
    rd = DateTable(date=selectDate)
    dateSelect = NewDateForm(instance=rd)

    #         {% for time in times %}
    #     <tr>
    #         <td>{{ time }}</td>
            
    #         {% for x in companyLinkTable %}
    #             {% if x.dateID.date == selectDate %}
    #                 {% if x.startTime.hour == time %}
    #                     <td>{{ x.dateID.attendeeID.fName }} {{ x.dateID.attendeeID.lName }}</td>
    #                     <td>{{ x.companyID.name }}</td>
    #                     <td>{{ x.startTime }} - {{ x.endTime }}</td><br>
    listForDash = []
    index = 0
    prevTime = 9
    for time in times:
        thistime = False
        for x in companyLinkTable:
            if x.dateID.date == selectDate:

                # All 'company links' within specific  day
                if x.startTime.hour == time:
                    if time == prevTime:
                        #print()
                        listForDash[index].append([x.dateID.attendeeID.fName, x.dateID.attendeeID.lName, x.companyID.name, x.startTime, x.endTime])
                    else:
                        #print(x.dateID.attendeeID.fName, x.startTime.hour)
                        listForDash.append([time, [x.dateID.attendeeID.fName, x.dateID.attendeeID.lName, x.companyID.name, x.startTime, x.endTime]])
                        prevTime = time
                    thistime=True
                    
                    #thistime = True
                    #listForDash += [[time, x.dateID.attendeeID.fName, x.dateID.attendeeID.lName, x.companyID.name, x.startTime, x.endTime]]
        if thistime == False:
            listForDash.append([time])
        
        index += 1
        

    #         {% for x in companyLinkTable %}
    #     {% if x.dateID.date == selectDate %}
    #         <tr><td><a href="{% url 'attendeeView' x.dateID.attendeeID event.eventID %}">{{ x.dateID.attendeeID.fName }} {{ x.dateID.attendeeID.lName }}</a></td></tr>
    #     {% endif %}
    # {% endfor %}

    listOfPeople = []

    for x in companyLinkTable:
        if x.dateID.date == selectDate:
            if len(listOfPeople) > 0:
                for person in listOfPeople:
                    if x.dateID.attendeeID != person[0]:
                        listOfPeople.append([x.dateID.attendeeID, [x.dateID.attendeeID.fName, x.dateID.attendeeID.lName]])
            else:
                listOfPeople.append([x.dateID.attendeeID, [x.dateID.attendeeID.fName, x.dateID.attendeeID.lName]])
    print(listOfPeople)
    return render(request, 'dashboard.html', {"listOfPeople": listOfPeople, "listForDash":listForDash ,"selectDate": selectDate, "dateSelect": dateSelect, "event": event, "times": times, "companyLinkTable": companyLinkTable})


def goToAttendees(request, attendeeID, eventID):
    if attendeeID.isdigit():
        res = attendeeID
    else:
        res = re.search(r'\((.*?)\)',attendeeID).group(1)
    attendee = AttendeeTable.objects.get(pk=res)
    dates = DateTable.objects.filter(attendeeID=res)
    accomplices = AccompliceTable.objects.filter(attendeeID=res)
    emails = EmailTable.objects.filter(attendeeID=res)

    #event = EventTable.objects.get(pk=eventID)
    stages = []
    for date in dates:
        companyLinkTable = CompanyLinkTable.objects.filter(eventID=eventID, dateID=date)
        stages += companyLinkTable

    return render(request, 'attendee.html', {"eventID": eventID, "companyLinkTable": companyLinkTable, "attendee": attendee, "dates": dates, "accomplices": accomplices, "emails": emails})

def changeDate(request, attendeeID, eventID, dateID):
    date = DateTable.objects.get(pk=dateID)
    dateSelect = NewDateForm(request.POST or None, instance=date)
    
    if dateSelect.is_valid():
        dateSelect.save()
        return redirect('attendeeView', attendeeID, eventID)

    return render(request, 'newdate.html', {"dateSelect": dateSelect})
    

def updateAttendance(request, attendeeID, eventID):
    if attendeeID.isdigit():
        res = attendeeID
    else:
        res = re.search(r'\((.*?)\)',attendeeID).group(1)

    attendee = AttendeeTable.objects.get(pk=res)
    form = UpdateAttendanceForm(request.POST or None, instance=attendee)
    if form.is_valid():
        form.save()
        return redirect('attendeeView', attendeeID, eventID)

    return render(request, "updateattendance.html", {"form": form})


def updateAccomplice(request, attendeeID, eventID, accompliceID):
    accomplice = AccompliceTable.objects.get(pk=accompliceID)
    form = UpdateAccompliceForm(request.POST or None, instance=accomplice)
    if form.is_valid():
        form.save()
        return redirect('attendeeView', attendeeID, eventID)
    return render(request, "updateaccomplice.html", {"form": form})

def addStage(request, attendeeID, eventID):
    acompany = CompanyLinkTable.objects.filter(eventID=eventID).first()
    ac = CompanyTable.objects.filter(companyID=acompany.companyID)
    form = AddStageForm(ac)
    return render(request, "addstage.html", {"form": form})