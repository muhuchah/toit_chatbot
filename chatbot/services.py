from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from chatbot.models import User, Chatbot, Chat, Message, Chatbot_data, Comment
from chatbot.forms import ChatbotForm, ChatbotDataForm
from openai import OpenAI
from django.core.paginator import Paginator


# Variables
API_KEY = "dWJ6TR1Wdo39SYxHqgYh60i7fjKnaPlO"
BASE_URL = "https://openai.torob.ir/v1"

def openai_response(usermessage, data):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    content = f"Based on the specific data: {data}, answer to the following question."
    

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": usermessage}
        ]
    )

    return completion.choices[0].message.content


def openai_generate_title(user_message):
    # Handle Prompt
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot, skilled in answering user's questions, generate a good and small (under 16 characters) title for the user message"},
            {"role": "user", "content": user_message}
        ]
    )
   
    return completion.choices[0].message.content


def create_embedding(data):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = client.embeddings.create(
        input = data,
        model = 'text-embedding-ada-002',
        encoding_format = 'float'
    )

    return response.data[0].embedding