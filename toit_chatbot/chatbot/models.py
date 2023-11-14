from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    can_make_chatbot = models.BooleanField(default=False)

class Chatbot(models.Model):
    name = models.CharField(max_length=30)
    bio = models.CharField(max_length=100)
    # chatbot image
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Chatbot_data(models.Model):
    data = models.CharField(max_length=800)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)

class Chat(models.Model):
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.CharField(max_length=100)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.BooleanField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)