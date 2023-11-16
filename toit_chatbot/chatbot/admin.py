from django.contrib import admin

from .models import User, Chatbot, Chat, Message

admin.site.register(User)
admin.site.register(Chatbot)
admin.site.register(Chat)
admin.site.register(Message)