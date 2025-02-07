import time
from django.shortcuts import render
from .forms import GmailCredentialsForm
import sys
from .path_utils import get_path2file_getMessages

path2file_getMessages = get_path2file_getMessages()
sys.path.append(str(path2file_getMessages.parent))
from getMessages import read_emails


# Create your views here.
def index(request):
    return render(request, 'messages/index.html')


def messages_list(request):
    got_messages = False
    messages = {}
    if request.method == "POST":
        form = GmailCredentialsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['gmail']
            password = cd['oauth2_key']
            # time.sleep(1)
            messages = read_emails(email, password)
            if messages:
                got_messages = True
                messages = dict(reversed(list(messages.items())))
    else:
        form = GmailCredentialsForm()
    return render(request,
                  'messages/messages_list.html',
                  {'messages': messages,
                   'got_messages': got_messages,
                   'form': form})


def concrete_message(request):
    return None


def help2OAuth2Key(request):
    return render(request, 'messages/help.html')
