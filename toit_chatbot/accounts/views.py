from django.shortcuts import render, redirect
from django.contrib import messages
from chatbot.models import User

def home(request):
    return render(request, "accounts/index.html")

def signup(request):
    if request.mothod == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if len(username)>30:
            messages.error(request, "Username must be under 30 charcters!!")
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")

        myuser = User.objects.create(username, pass1)
        myuser.save()

        return redirect('signin')

    return render(request, "accounts/signin.html")


def authenticate(username, password):
    if User.objects.filter(username=username):
        if User.objects.filter(username=username).password != password:
            return False
    else:
        return False

    return True

def signin(request):
    if request.methon == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if authenticate(username, password):
            ... # return render(request, "chatbot_list")
        else:
            messages.error(request, "Try Again!")
            return redirect('home')
    
    return render(request, "accounts/signin.html")

def signout(request):
    ...