from django.shortcuts import render, redirect
from django.contrib import messages
from chatbot.models import User

def home(request):
    return render(request, "accounts/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password-confirm']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if len(username)>30:
            messages.error(request, "Username must be under 30 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        myuser = User(username=username, password=pass1)
        myuser.save()

        return redirect('signin')

    return render(request, "accounts/signup.html")


def authenticate_user(username, password):
    if User.objects.filter(username=username):
        myuser = User.objects.get(username=username)
        if myuser.password == password:
            return {"user":myuser}

    return {}


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        myuser = authenticate_user(username, password)
        if myuser:
            return render(request, "chatbot/index.html", myuser)
        else:
            messages.error(request, "Try Again!")
            return redirect('home')
    
    return render(request, "accounts/signin.html")