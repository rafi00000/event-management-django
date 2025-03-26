from django.shortcuts import render, redirect
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("form not valid")
    
    context = {
        "registerForm": form
    }
    return render(request, "registerforms/register.html", context)

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home-page")
    context={
        "login_form": form
    }
    return render(request, "registerforms/login.html", context)

def sign_out(request):
    pass