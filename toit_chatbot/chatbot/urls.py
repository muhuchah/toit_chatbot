from django.urls import path

from . import views

urlpatterns = [
    path('chatbots_list/<int:user_id>/', views.chatbots_list, name='chatbots_list'),
    path('mychatbots_list/<int:user_id>/', views.mychatbots_list, name='mychatbots_list'),
    path('chat_history/<int:user_id>/<int:chatbot_id>/', views.chat_history, name='chat_history'),
    path('chat_detail/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('create_newchat/<int:user_id>/<int:chatbot_id>/', views.create_newchat, name='create_newchat'),
    path('signout/', views.signout, name='signout'),
]