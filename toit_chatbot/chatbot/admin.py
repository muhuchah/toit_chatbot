from django.contrib import admin

from .models import User, Chatbot, Chat

admin.site.register(User)
admin.site.register(Chatbot)
admin.site.register(Chat)