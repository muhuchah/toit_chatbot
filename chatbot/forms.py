from django import forms
from chatbot.models import Chatbot, Chatbot_data

class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = ['name', 'bio', 'is_enable']