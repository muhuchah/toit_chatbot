from django.urls import path

from . import views

urlpatterns = [
    path('chatbots_list/', views.chatbots_list, name='chatbots_list'),
    path('chat_history/<int:user_id>/<int:chatbot_id>/', views.chat_history, name='chat_history'),
    path('signout/', views.signout, name='signout'),
]