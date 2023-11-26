from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message, Chatbot_data, Comment
from chatbot.forms import ChatbotForm
from chatbot.services import openai_response, openai_generate_title, create_embedding
from pgvector.django import CosineDistance
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import F


def chatbots_list(request, user_id):
    user = get_object_or_404(User, id=user_id)

    NUMBER_OF_CHATBOTS_PER_PAGE = 10
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

    NUMBER_OF_CHATBOTS_PER_PAGE = 10
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
    
    NUMBER_OF_CHATS_PER_PAGE = 10
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
        user_message_embed = create_embedding(user_message)

        chatbot = chat.chatbot
        nearest_data = chatbot.chatbot_data_set.order_by(CosineDistance('embedding', user_message_embed))[:1]

        chatbot_response = openai_response(usermessage=user_message, data=nearest_data, sys_prompt=chatbot.system_prompt)
        
        message = Message(user_message=user_message, chatbot_response=chatbot_response, chat=chat)
        message.save()
        message.search_vector = (
            SearchVector('user_message', weight='A')
            + SearchVector('chatbot_response', weight='B')
        )
        message.save()

    # q is the search query
    q = request.GET.get('q')

    if not q:
        messages = chat.message_set.all()
    else:
        query = SearchQuery(q)

        messages = chat.message_set.annotate(rank=SearchRank(F('search_vector'), query)).filter(rank__gte=0.001).order_by('-rank')


    if len(messages) == 1 and not q:
        chat.title = openai_generate_title(user_message)
        chat.save()


    context = {
        'chat': chat,
        'messages': messages
    }

    return render(request, 'chatbot/chat_detail.html', context)


def chatbot_detail(request, chatbot_id):
    chatbot = Chatbot.objects.get(id=chatbot_id)
    
    chatbot_dataset = chatbot.chatbot_data_set.all()

    if chatbot:
        initial_chatbot_data = {
            'name': chatbot.name,
            'bio': chatbot.bio,
            #'image': chatbot.image,
            'is_enable': chatbot.is_enable,
            'system_prompt': chatbot.system_prompt
        }
        chatbot_form = ChatbotForm(initial=initial_chatbot_data)

    else:
        chatbot_form = ChatbotForm()
    
    if request.method == 'POST':
        chatbot_form = ChatbotForm(request.POST, instance=chatbot)
        chatbot_form.save()

    context = {
        'chatbot_form': chatbot_form,
        'chatbot': chatbot,
        'data_forms': chatbot_dataset
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


def create_new_data(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)
    data = request.POST['chatbot_data']

    if data:
        embedding = create_embedding(data)

        new_data = Chatbot_data(data=data, embedding=embedding, chatbot=chatbot)
        new_data.save()

    
    return redirect('chatbot_detail', chatbot_id=chatbot_id)


def edit_chatbot_data(request, chatbot_id):
    if request.method == 'POST':
        chatbot_data_id = request.POST['form_id']
        chatbot_data = get_object_or_404(Chatbot_data, id=chatbot_data_id)
        chatbot = chatbot_data.chatbot

        data = request.POST['chatbot_data_'+str(chatbot_data_id)]
        chatbot_data.data = data
        chatbot_data.embedding = create_embedding(data=data)
        chatbot_data.save()
    else:
        print(request.GET)

    return redirect('chatbot_detail', chatbot_id=chatbot.id)


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
        user_message_embed = create_embedding(message.user_message)

        nearest_data = chatbot.chatbot_data_set.order_by(CosineDistance('embedding', user_message_embed))[:1]

        response = openai_response(message.user_message, data=nearest_data, sys_prompt=chatbot.system_prompt)
        #response = "THIS IS A TEST ANSWER TO YOUR DISLIKE TO THIS IS A TEST ANSWER"

        new_message = Message(user_message=message.user_message, chatbot_response=response, chat=chat)
        new_message.save()

    return redirect('chat_detail', chat_id=chat.id)