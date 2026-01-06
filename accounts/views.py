
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Login page ke input name
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')  # Login ke baad home page
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, 'accounts/login.html')
def SignupPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if password1 != password2:
            return HttpResponse("Passwords do not match")
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered")
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect("login")
    
    return render(request, "accounts/signup.html")


def LogoutPage(request):
    logout(request)
    return redirect('login')
