from django.contrib import admin

from .models import User, Chatbot, Chat, Message, Comment, Chatbot_data

admin.site.register(User)
admin.site.register(Chatbot)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Chatbot_data)