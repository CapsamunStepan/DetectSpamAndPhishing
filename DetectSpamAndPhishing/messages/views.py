from django.shortcuts import render, redirect, HttpResponse
from .forms import GmailCredentialsForm
from .models import GmailUser, GmailMessage
from .get_messages import read_emails, get_total_messages_count, check_OAuth2key
import random
from email.utils import parsedate_to_datetime
from django_q.tasks import async_task


def index(request):
    return render(request, 'messages/index.html')


def authenticate_user(request):
    form = GmailCredentialsForm(request.POST or None)
    is_credentials = False
    is_correct_credentials = False
    show_modal_window = random.random() < 0.1
    if request.session.get('gmail') and request.session.get('password'):
        is_credentials = True
    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        gmail = cd['gmail']
        password = cd['oauth2_key']
        is_correct_credentials = check_OAuth2key(gmail, password)  # выполняется около секунды
        if is_correct_credentials:
            request.session['gmail'] = gmail
            request.session['password'] = password
            user, _ = GmailUser.objects.get_or_create(gmail=gmail)
            is_credentials = True

    return render(request, 'messages/auth.html', {
        'is_credentials': is_credentials,
        'form': form,
        'show_modal_window': show_modal_window,
        'is_correct_credentials': is_correct_credentials,
    })


def load_more_messages(request):
    return None


def concrete_message(request):
    return None


def help2OAuth2Key(request):
    return render(request, 'messages/help.html')


def new_email_data(request):
    request.session.pop('gmail', None)
    request.session.pop('password', None)
    return redirect(to='messages:authenticate_user')


def messages_list(request):
    gmail = request.session.get('gmail')
    password = request.session.get('password')
    if not (gmail and password):
        return redirect(to='messages:authenticate_user')
    limit = 15
    total_messages_count = get_total_messages_count(gmail, password)  # около 2 секунд
    user = GmailUser.objects.get(gmail=gmail)
    stored_messages = GmailMessage.objects.filter(receiver=user)
    stored_messages_ids = [message.gmail_id for message in stored_messages]
    request.session['last_loaded_message_id'] = total_messages_count - limit

    new_messages_ids = [str(x).encode() for x in range(total_messages_count, total_messages_count - limit, -1)
                        if x not in stored_messages_ids]

    if new_messages_ids:
        messages = read_emails(gmail, password, new_messages_ids)
        if messages:
            for id_, msg in messages.items():
                GmailMessage.objects.create(
                    gmail_id=int(id_),
                    subject=msg['Subject'],
                    body=msg['Body'],
                    sender=msg['From'],
                    receiver=user,
                    received_at=parsedate_to_datetime(msg['Date']),
                )

    stored_messages = GmailMessage.objects.filter(receiver=user)

    return render(request, 'messages/messages_list.html',
                  {
                      'got_messages': True,
                      'messages': stored_messages,
                      'total_messages': total_messages_count,
                      'loaded_messages': 15,
                  })


def vulnerabilities_list(request):
    return render(request, 'messages/vulnerabilities.html')


def training_materials(request):
    return render(request, 'messages/training_materials.html')


def delivery_threats(request):
    return render(request, 'messages/delivery_threats.html')
