from django.urls import path

from . import views

urlpatterns = [
    path('chatbots_list/', views.chatbots_list, name='chatbots_list'),
    path('signout/', views.signout, name='signout'),
]