from django.db import models
from django.contrib.auth.models import User




class Chat (models.Model):
    
    roomname  = models.CharField(blank=True , max_length=50)
    members = models.ManyToManyField(User , null=True , blank=True)

    def __str__(self):
        return self.roomname





class Message(models.Model):
    
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    related_chat = models.ForeignKey(Chat , on_delete=models.CASCADE , blank=True , null=True)
    
    def last_message(self , roomname):
        #return Message.objects.order_by("-create_time").all()
        return Message.objects.filter(related_chat__roomname = roomname)
    
    def __str__(self):
        return self.author.username 
    
