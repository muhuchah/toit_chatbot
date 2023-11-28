from django.db import models
from pgvector.django import VectorField
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    can_make_chatbot = models.BooleanField(default=False)
    chatbots = models.ManyToManyField('Chatbot', through='Chat')

class Chatbot(models.Model):
    name = models.CharField(max_length=30)
    bio = models.CharField(max_length=100)
    # chatbot image
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_enable = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    system_prompt = models.CharField(default="Based on the specific data: {data}, answer to the following question.")

class Chatbot_data(models.Model):
    data = models.CharField(max_length=800)
    embedding = VectorField(dimensions=1536)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)

class Chat(models.Model):
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    chat_history = models.CharField(max_length=2048)

class Message(models.Model):
    user_message = models.CharField(max_length=1024)
    chatbot_response = models.CharField(max_length=4096)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    search_vector = SearchVectorField(default=None, null=True)


class Comment(models.Model):
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def clean(self):
        if self.like and self.dislike:
            raise ValidationError("Like and dislike cannot be true at the same time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Trigger validation
        super().save(*args, **kwargs)