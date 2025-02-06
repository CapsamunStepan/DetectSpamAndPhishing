from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.index, name='index'),
    path('messages/', views.messages_list, name='messages'),
    path('help/', views.help2OAuth2Key, name='help'),
]