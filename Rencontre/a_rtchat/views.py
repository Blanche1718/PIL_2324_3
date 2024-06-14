<<<<<<< HEAD
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm

# Create your views here.

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="Angela")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.group = chat_group
            message.save()
            return redirect('connexion')
            
            

    return render(request, 'chat.html', {'chat_messages' : chat_messages})
=======
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="Angela")
    chat_messages = chat_group.chat_messages.all()[:30]
    return render(request, 'a_rtchat/chat.html', {'chat_messages' : chat_messages})
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4

