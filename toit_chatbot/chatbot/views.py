from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message, Chatbot_data
from chatbot.forms import ChatbotForm, ChatbotDataForm
from openai import OpenAI
from django.core.paginator import Paginator

API_KEY = "dWJ6TR1Wdo39SYxHqgYh60i7fjKnaPlO"
BASE_URL = "https://openai.torob.ir/v1"

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
        text = request.POST['usermessage']

        usermessage = Message(text=text, chat=chat, user_message=True)
        usermessage.save()

        # Handle Prompt
        """
        client = OpenAI(api_key='API_KEY', base_url='BASE_URL')

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                #{"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": usermessage}
            ]
        )
        """
        #text = completion.choices[0].message
        text = "THIS IS A TEST ANSWER!"
        chatbot_message = Message(text=text, chat=chat, user_message=False)
        chatbot_message.save()


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
        'user_id': chatbot.owner.id,
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


def create_newchatbot(request, user_id):
    user = get_object_or_404(User, id=user_id)

    newchatbot = Chatbot(owner=user, name='New chatbot', bio='I am a new chatbot')
    newchatbot.save()

    return redirect('chatbot_detail', chatbot_id=newchatbot.id)


def signout(request):
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')