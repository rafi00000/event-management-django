from django.shortcuts import render, redirect
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "Account created successfully. Please check your email to activate your account.")
            return redirect("sign-in")
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
    logout(request)
    return redirect("home-page")


def activate_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully.")
            return redirect("sign-in")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("sign-up")