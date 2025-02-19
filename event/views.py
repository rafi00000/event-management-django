from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import CreateEventForm
from django.contrib import messages
from event.models import Event
from datetime import date


# Create your views here.

def home(request):
    return render(request, "home.html")


def organizer_dashboard(request):
    date_today = date.today()
    today_events = Event.objects.filter(date=date_today)
    print(today_events)
    context = {
        "today_events": today_events
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
