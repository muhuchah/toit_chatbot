from django import forms
from chatbot.models import Chatbot, Chatbot_data

class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = '__all__'


class ChatbotDataForm(forms.ModelForm):
    class Meta:
        model = Chatbot_data
        fields = '__all__'