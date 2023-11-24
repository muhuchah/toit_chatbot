from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message, Chatbot_data, Comment
from chatbot.forms import ChatbotForm, ChatbotDataForm
from chatbot.services import openai_response, openai_generate_title, create_embedding
from openai import OpenAI
import json
from django.core.paginator import Paginator



def chatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)

    NUMBER_OF_CHATBOTS_PER_PAGE = 1
    p = Paginator(Chatbot.objects.all(), NUMBER_OF_CHATBOTS_PER_PAGE)
    page = request.GET.get('page')
    chatbots = p.get_page(page)
    
    context = {
        "chatbots" : chatbots,
        "user": user
    }

    return render(request, "chatbot/chatbots_list.html", context)


def mychatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)

    NUMBER_OF_CHATBOTS_PER_PAGE = 1
    p = Paginator(user.chatbot_set.all(), NUMBER_OF_CHATBOTS_PER_PAGE)
    page = request.GET.get('page')
    chatbots = p.get_page(page)

    context = {
        "user_id": user.id,
        "chatbots": chatbots,
    }

    return render(request, 'chatbot/mychatbots_list.html', context)


def chat_history(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)

    if not chatbot.is_enable:
        return redirect('chatbots_list', user_id)
    
    NUMBER_OF_CHATS_PER_PAGE = 1
    p = Paginator(Chat.objects.filter(user=user, chatbot=chatbot).values_list('title', 'id'), NUMBER_OF_CHATS_PER_PAGE)
    page = request.GET.get('page')
    chats_info = p.get_page(page)

    context = {
        'user_id': user.id,
        'chatbot_id': chatbot.id,
        'chatbot_name': chatbot.name,
        'chats_info': chats_info
    }

    return render(request, "chatbot/chat_history.html", context)


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id) 

    if not chat.chatbot.is_enable:
        return redirect('chatbots_list', chat.user.id)

    if request.method == 'POST':
        user_message = request.POST['usermessage']

        chatbot_response = openai_response(user_message)
        #chatbot_response = "THIS IS A TEST ANSWER!"
        
        message = Message(user_message=user_message, chatbot_response=chatbot_response, chat=chat)
        message.save()


    messages = chat.message_set.all()

    if len(messages) == 1:  # new chat need a new title
        chat.title = openai_generate_title(user_message)
        #chat.title = "TEST TITLE"
        chat.save()


    context = {
        'chat': chat,
        'messages': messages
    }

    return render(request, 'chatbot/chat_detail.html', context)


def chatbot_detail(request, chatbot_id):
    chatbot = Chatbot.objects.get(id=chatbot_id)
    chatbot_data_forms = []
    if chatbot:
        initial_chatbot_data = {
            'name': chatbot.name,
            'bio': chatbot.bio,
            #'image': chatbot.image,
            'chatbot_state': chatbot.is_enable
        }
        chatbot_form = ChatbotForm(initial=initial_chatbot_data)

        chatbot_dataset = chatbot.chatbot_data_set.all()
        if chatbot_dataset:
            for chatbot_data in chatbot_dataset:
                initial_chatbot_data = {
                    'data': chatbot_data.data,
                }
                chatbot_data_form = ChatbotDataForm(initial=initial_chatbot_data, prefix=str(chatbot_data.id))

                chatbot_data_forms.append(chatbot_data_form)
        else:
            chatbot_data = Chatbot_data(chatbot=chatbot)
            initial_chatbot_data = {
                'data': "Your Data",
            }
            chatbot_data_form = ChatbotDataForm(initial=initial_chatbot_data, prefix=str(chatbot_data.id))

            chatbot_data_forms.append(chatbot_data_form)
    else:
        chatbot_form = ChatbotForm()

    if request.method == 'POST':
            chatbot_form = ChatbotForm(request.POST)#, request.FILES)

            for chatbot_data_form in chatbot_data_forms:
                if chatbot_data_form.prefix in request.POST:
                    # The form with a matching prefix is the submitted form
                    submitted_form = chatbot_data_form
                    break
    
            chatbot_data_form = ChatbotDataForm(request.POST)

            chatbot.name = chatbot_form.data['name']
            chatbot.bio = chatbot_form.data['bio']
            #chatbot.image = chatbot_form.cleaned_data['image']
            chatbot.is_enable = chatbot_form.data['chatbot_state']
            chatbot.save()

            chatbot_data = chatbot.chatbot_data_set.get(id=int(submitted_form.prefix))
            chatbot_data.data = submitted_form.data['data']
            chatbot_data.embedding = create_embedding(chatbot_data.data)
            chatbot_data.save()

            return redirect('chatbot_detail', chatbot_id=chatbot_id)

    context = {
        'user_id': chatbot.owner.id,
        'chatbot_form': chatbot_form,
        'chatbot_data_forms': chatbot_data_forms,
    }

    return render(request, 'chatbot/chatbot_detail.html', context)


def create_newchat(request, user_id, chatbot_id):
    user = get_object_or_404(User, id=user_id)
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)

    mychat = Chat(user=user, chatbot=chatbot, title="NewChat")
    mychat.save()

    return redirect('chat_detail', chat_id=mychat.id)


def create_newchatbot(request, user_id):
    user = get_object_or_404(User, id=user_id)

    newchatbot = Chatbot(owner=user, name='New chatbot', bio='I am a new chatbot')
    newchatbot.save()

    return redirect('chatbot_detail', chatbot_id=newchatbot.id)


def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def like_dislike(request, is_like, chat_id, message_id):
    chat = get_object_or_404(Chat, id=chat_id)
    message = get_object_or_404(Message, id=message_id)

    chatbot = get_object_or_404(Chatbot, id=chat.chatbot.id)
    comment = message.comment_set.first()
    if comment:
        if is_like == 1:
            if comment.dislike:
                comment.like = True
                chatbot.likes += 1
                comment.dislike = False
                chatbot.dislikes -= 1
            elif not comment.dislike and not comment.like:
                comment.like = True
                chatbot.likes += 1
        else: # dislike
            if comment.like:
                comment.like = False
                chatbot.likes -= 1
                comment.dislike = True
                chatbot.dislikes += 1
            elif not comment.like and not comment.dislike:
                comment.dislike = True
                chatbot.dislikes += 1
    else:
        if is_like == 1:
            comment = Comment(message=message, like=True, dislike=False)

            chatbot.likes += 1
        else:
            comment = Comment(message=message, like=False, dislike=True)

            chatbot.dislikes += 1

    comment.save()
    chatbot.save()

    if is_like != 1:
        # generate another response to the message
        response = openai_response(message.user_message)
        #response = "THIS IS A TEST ANSWER TO YOUR DISLIKE TO THIS IS A TEST ANSWER"

        new_message = Message(user_message=message.user_message, chatbot_response=response, chat=chat)
        new_message.save()

    return redirect('chat_detail', chat_id=chat.id)