from django.urls import path

from . import views

urlpatterns = [
    path('chatbots_list/', views.chatbots_list, name='chatbots_list'),
    path('chat_history/<int:user_id>/<int:chatbot_id>/', views.chat_history, name='chat_history'),
    path('chat_detail/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('signout/', views.signout, name='signout'),
]