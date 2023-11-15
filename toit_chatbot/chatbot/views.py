from django.shortcuts import render, redirect
from django.contrib import messages
from chatbot.models import Chatbot

def chatbots_list(request):
    chatbots = Chatbot.objects.all()
    
    context = {
        "chatbots" : chatbots
    }

    return render(request, "chatbot/chatbots_list.html", context)

def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')