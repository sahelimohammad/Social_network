from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from . import models
import json



@login_required(login_url='account:user_login')
def index(request):
    user = request.user
    chat_rooms = models.Chat.objects.filter(members = user)
    context = {
        "chat_rooms" : chat_rooms
    }
    
    return  render(request , "chat/index.html" , context=context)




@login_required(login_url='account:user_login')
def room(request , room_name):
    
    chat_room = models.Chat.objects.filter(roomname = room_name)

    if  not chat_room.exists():
        chat_model = models.Chat.objects.create(roomname = room_name)
        chat_model.members.add(request.user)
        chat_model.save()
    else :
        chat_room[0].members.add(request.user)
    
    
    username = request.user.username
    
    context = {
        'room_name': room_name ,
        'username' : mark_safe(json.dumps(username))
    }
    return render(request , "chat/room.html" , context=context)