from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message, Chatbot_data
from chatbot.forms import ChatbotForm, ChatbotDataForm

def chatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    chatbots = Chatbot.objects.all()
    
    context = {
        "chatbots" : chatbots,
        "user": user
    }

    return render(request, "chatbot/chatbots_list.html", context)


def mychatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)

    chatbots = user.chatbot_set.all()

    context = {
        "chatbots": chatbots,
    }

    return render(request, 'chatbot/mychatbots_list.html', context)


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


def chatbot_detail(request, chatbot_id):
    print(request.method)
    chatbot = Chatbot.objects.get(id=chatbot_id)
    if chatbot:
        initial_chatbot_data = {
            'name': chatbot.name,
            'bio': chatbot.bio,
            #'image': chatbot.image,
            'chatbot_state': chatbot.is_enable
        }
        chatbot_form = ChatbotForm(initial=initial_chatbot_data)

        chatbot_data = chatbot.chatbot_data_set.first()
        if chatbot_data:
            initial_chatbot_data = {
                'data': chatbot_data.data
            }
            chatbot_data_form = ChatbotDataForm(initial=initial_chatbot_data)
        else:
            chatbot_data = Chatbot_data(chatbot=chatbot)
            chatbot_data_form = ChatbotDataForm()
    else:
        chatbot_form = ChatbotForm()

    if request.method == 'POST':
            print("---------------")
            print(request.POST)
            print("---------------")
            chatbot_form = ChatbotForm(request.POST)#, request.FILES)
            chatbot_data_form = ChatbotDataForm(request.POST)

            chatbot.name = chatbot_form.data['name']
            chatbot.bio = chatbot_form.data['bio']
            #chatbot.image = chatbot_form.cleaned_data['image']
            chatbot.is_enable = chatbot_form.data['chatbot_state']
            chatbot.save()

            chatbot_data.data = chatbot_data_form.data['data']
            chatbot_data.save()

            return redirect('chatbot_detail', chatbot_id=chatbot_id)

    context = {
        'chatbot_id': chatbot_id,
        'chatbot_form': chatbot_form,
        'chatbot_data_form': chatbot_data_form,
    }

    return render(request, 'chatbot/chatbot_detail.html', context)


def create_newchat(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)

    mychat = Chat(user=user, chatbot=chatbot, title="NewChat")
    mychat.save()

    return redirect('chat_detail', chat_id=mychat.id)


def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')