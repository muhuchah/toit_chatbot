from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message

def chatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    chatbots = Chatbot.objects.all()
    
    context = {
        "chatbots" : chatbots,
        "user": user
    }

    return render(request, "chatbot/chatbots_list.html", context)


def chat_history(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)
    
    chats_info = Chat.objects.filter(user=user, chatbot=chatbot).values_list('title', 'id')

    context = {
        'user_id': user.id,
        'chatbot_id': chatbot.id,
        'chatbot_name': chatbot.name,
        'chats_info': chats_info
    }

    return render(request, "chatbot/chat_history.html", context)


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id) 
    
    if request.method == 'POST':
        text = request.POST['usermessage']

        usermessage = Message(text=text, chat=chat, user_message=True)
        usermessage.save()

        # Handle Prompt

    messages = chat.message_set.all()

    context = {
        'chat': chat,
        'messages': messages
    }

    return render(request, 'chatbot/chat_detail.html', context)


def create_newchat(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)

    mychat = Chat(user=user, chatbot=chatbot, title="NewChat")
    mychat.save()

    return redirect('chat_detail', chat_id=mychat.id)


def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')