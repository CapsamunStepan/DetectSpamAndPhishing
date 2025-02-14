from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.index, name='index'),
    path('authenticate/', views.authenticate_user, name='authenticate_user'),
    path('load_more/', views.load_more_messages, name='load_more_messages'),
    path('help/', views.help2OAuth2Key, name='help'),
    path('new_email_credentials/', views.new_email_data, name='new_email_data'),
    path('messages_list/', views.messages_list, name='messages_list'),
]