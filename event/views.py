from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def organizer_dashboard(request):
    context = {

    }
    return render(request, "dashboard.html", context)   