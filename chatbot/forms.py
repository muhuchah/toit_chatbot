from django import forms
from chatbot.models import Chatbot

class ChatbotForm(forms.ModelForm):
    system_prompt = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Chatbot
        fields = ['name', 'bio', 'is_enable', 'system_prompt']