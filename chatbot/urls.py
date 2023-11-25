from django.urls import path

from . import views

urlpatterns = [
    path('chatbots_list/<int:user_id>/', views.chatbots_list, name='chatbots_list'),
    path('mychatbots_list/<int:user_id>/', views.mychatbots_list, name='mychatbots_list'),
    path('chat_history/<int:user_id>/<int:chatbot_id>/', views.chat_history, name='chat_history'),
    path('chat_detail/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('create_newchat/<int:user_id>/<int:chatbot_id>/', views.create_newchat, name='create_newchat'),
    path('create_newchatbot/<int:user_id>/', views.create_newchatbot, name='create_newchatbot'),
    path('create_new_data/<int:chatbot_id>/', views.create_new_data, name='create_new_data'),
    path('chatbot_detail/<int:chatbot_id>/', views.chatbot_detail, name='chatbot_detail'),
    path('chatbot_detail/<int:chatbot_id>/edit_chatbot_data/', views.edit_chatbot_data, name='edit_chatbot_data'),
    path('like_dislike/<int:is_like>/<int:chat_id>/<int:message_id>/', views.like_dislike, name='like_dislike'),
    path('signout/', views.signout, name='signout'),
]