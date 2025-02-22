from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import CreateEventForm, AddParticipants, AddCategory
from django.contrib import messages
from event.models import Event, Participant
from datetime import date
from django.db.models import Count


# Create your views here.

def home(request):
    return render(request, "home.html")


def organizer_dashboard(request):
    date_today = date.today()
    today_events = Event.objects.filter(date=date_today)
    total_participant = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt = date_today).count()
    past_events = Event.objects.filter(date__lt=date_today).count()
    print(total_participant)
    context = {
        "total_events": total_events,
        "today_events": today_events,
        "participant_count": total_participant,
        "upcoming_events": upcoming_events,
        "past_events": past_events
    }
    return render(request, "dashboard.html", context)   

def create_task(request):
    event_form = CreateEventForm()
    if request.method == "POST":
        event_form = CreateEventForm(request.POST)
        if event_form.is_valid():
            event_form.save()   
            messages.success(request, "Event created Successfully")
            return redirect("create-event")
            
    context = {
        "event_form": event_form
    }
    return render(request, "create-event.html", context)


def addParticipant(request):
    participant_form = AddParticipants()

    if request.method == "POST":
        participant_form = AddParticipants(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Added")
            return redirect("add-participant")
    
    context = {
        "add_participant_form" : participant_form
    }
    return render(request, "add_participant.html", context)


def addCategory(request):
    addCateg = AddCategory()
    if request.method == "POST":
        addCateg = AddCategory(request.POST)
        if addCateg.is_valid():
            addCateg.save()
            messages.success(request, "Successfully Added")
            return redirect("add-category")
    context = {
        "category_form": addCateg
    }
    return render(request, "addCategory.html", context)