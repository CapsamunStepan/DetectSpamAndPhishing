from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'messages/index.html')


def messages_list(request):
    return render(request, 'messages/messages_list.html')


def concrete_message(request):
    return None
