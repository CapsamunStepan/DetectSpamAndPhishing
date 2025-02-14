from django.shortcuts import render, redirect, HttpResponse
from .forms import GmailCredentialsForm
from .get_messages import read_emails
import random


def index(request):
    return render(request, 'messages/index.html')


def authenticate_user(request):
    form = GmailCredentialsForm(request.POST or None)
    is_credentials = False
    show_modal_window = random.random() < 0.1
    if request.session.get('email') and request.session.get('password'):
        is_credentials = True
    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        email = cd['gmail']
        password = cd['oauth2_key']
        request.session['email'] = email
        request.session['password'] = password
        is_credentials = True

    return render(request, 'messages/auth.html', {
        'is_credentials': is_credentials,
        'form': form,
        'show_modal_window': show_modal_window
    })


def load_more_messages(request):
    return None


def concrete_message(request):
    return None


def help2OAuth2Key(request):
    return render(request, 'messages/help.html')


def new_email_data(request):
    request.session.pop('email', None)
    request.session.pop('password', None)

    return redirect(to='messages:authenticate_user')


def messages_list(request):
    # messages, total_messages = read_emails(request.session.get('email'), request.session.get('password'), 15)
    # got_messages = bool(messages)
    got_messages = True
    messages = {}
    total_messages = 40
    loaded_messages = len(messages)
    return render(request, 'messages/messages_list.html',
                  {'messages': messages,
                   'got_messages': got_messages,
                   'total_messages': total_messages,
                   'loaded_messages': loaded_messages, })
