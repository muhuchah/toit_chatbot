from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=50)

class Chatbot(models.Model):
    chatbot_name = models.CharField(max_length=50)
    chatbot_bio = models.CharField(max_length=300)
    # chatbot image
    chatbot_owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Chatbot_data(models.Model):
    data = models.CharField(max_length=1000)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)

class Chat(models.Model):
    ...

class Message(models.Model):
    message_text = models.CharField(max_length=200)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_text = models.BooleanField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)