from django import forms

class ChatbotForm(forms.Form):
    name = forms.CharField(max_length=32)
    bio = forms.CharField(widget=forms.Textarea)
    #image = forms.ImageField()
    chatbot_state = forms.BooleanField(widget=forms.RadioSelect(choices=[(True, 'Enabled'), (False, 'Disabled')]))


class ChatbotDataForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea)