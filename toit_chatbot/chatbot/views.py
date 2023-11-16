from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat

def chatbots_list(request):
    chatbots = Chatbot.objects.all()
    
    context = {
        "chatbots" : chatbots
    }

    return render(request, "chatbot/chatbots_list.html", context)


def chat_history(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)
    
    chats_info = Chat.objects.filter(user=user, chatbot=chatbot).values_list('title', 'id')
    print("-------------------------------")
    print(chats_info[0][0], chats_info[0][1])
    print("-------------------------------")

    context = {
        'chatbot_name': chatbot.name,
        'chats_info': chats_info
    }

    return render(request, "chatbot/chat_history.html", context)


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    return render(request, 'chatbot/chat_detail.html', {'chat': chat})


def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')