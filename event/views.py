from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import CreateEventForm
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, "home.html")


def organizer_dashboard(request):
    context = {
        
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
