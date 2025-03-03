from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import CreateEventForm, AddParticipants, AddCategory
from django.contrib import messages
from event.models import Event, Participant
from datetime import date, datetime
from django.db.models import Count, Sum



# Create your views here.

def home(request):
    # getting default and search by event result for home view
    query = request.GET.get('q', 'new')
    if query == 'new':
        search_event = Event.objects.select_related("category").prefetch_related("participant").all()
    else:
        search_event = Event.objects.select_related("category").prefetch_related("participant").filter(name__icontains=query).all()
    
    context = {
        "search_event": search_event,
    }
    print(f"search event: {search_event[0].participant.all()}")
    return render(request, "home.html", context)


def organizer_dashboard(request):
    today = date.today()
    today_date = f"{today}".split("-")
    print(f"today date: {today} => {today_date[0]}")
    total_participant = Participant.objects.aggregate(total=Count("id"))["total"]
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt = today).count()
    past_events = Event.objects.filter(date__lt=today).count()


    # getting data of events.
    q = request.GET.get("q")
    if q == "total_event":
        today_events = Event.objects.select_related("category").prefetch_related("participant").filter(date=today)
    elif q == "upcoming_event":
        today_events = Event.objects.select_related("category").prefetch_related("participant").filter(date=today)
    elif q == "past_event":
        today_events = Event.objects.select_related("category").prefetch_related("participant").filter(date=today)
    else:
        today_events = Event.objects.select_related("category").prefetch_related("participant").filter(date=today)

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

def update_task(request, id):
    event = Event.objects.get(id=id)
    event_form = CreateEventForm(instance=event)
    if request.method == "POST":
        event_form = CreateEventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated")
            return redirect("home-page")
    context = {
        "event_form": event_form
    }
    return render(request, "create-event.html", context)

def delete_task(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect("home-page")


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

def event_detail(request, id):
    event = Event.objects.get(id=id)
    context = {
        "event": event
    }
    return render(request, "event-detail.html", context)