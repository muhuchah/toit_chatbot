from django.shortcuts import render, redirect
from django.contrib import messages

def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')