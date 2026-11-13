import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import serializers , models
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

#user = get_user_model() مدل یوزر فعلی را برمیگرداند مدلش را فقط

class ChatConsumer(WebsocketConsumer):
    
    def new_message(self , data):
        #user = get_user_model()
        message = data["message"]
        username = data["username"]
        roomname = data["roomname"]
        self.notification(data)
        chat_model = models.Chat.objects.get(roomname=roomname)
        user_model = User.objects.filter(username=username).first()
        #user_model = user.objects.filter(username=username).first()
        message_model = models.Message.objects.create(author=user_model , content=message , related_chat = chat_model)
        result = eval(self.message_serializer(message_model))
        #result = eval(result)["content"]   
        self.send_to_chat_message(result)  
    
    
    
    def notification (self , data):
        roomname2 = data["roomname"]
        chat_model2 = models.Chat.objects.filter(roomname=roomname2)
        list = chat_model2[0].members.all()
        members_list = []
        for _ in list:
            members_list.append(_.username)
        
        async_to_sync(self.channel_layer.group_send)(
                "chat_listener", # مقصد پیام
                {"type": "chat_message",
                "content": data["message"],
                "__str__" : data["username"],
                "roomname" : roomname2 ,
                "members_list" : members_list
                }
        )


    
    def fetch_message(self , data):
        roomname = data["roomname"]
        queryset = models.Message.last_message(self , roomname)
        message_json = self.message_serializer(queryset)
        content = {
            "message" : eval(message_json),
            "command" : "fetch_message",

        }
        self.chat_message(content)
    
    
    
    def image(self , data):
        self.send_to_chat_message(data)
        
        
        
    
    commands = {
        "new_message" : new_message,
        "fetch_message" : fetch_message,
        "img" : image
    }
    

    
    
    def message_serializer(self , queryset):  
        
        serialized = serializers.MessageSerializer(queryset , many=(lambda queryset : True if (queryset.__class__.__name__ == "QuerySet") else False)(queryset)) 
        content = JSONRenderer().render(serialized.data)
        return content
        
        
 
    
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #message = text_data_json.get("message" , None)
        command = text_data_json["command"]
        #username = text_data_json.get("username" , None)
        self.commands[command](self , text_data_json) # برای فراخانی هر دوتا new_message و fetch_message در یک خط

    
    def send_to_chat_message(self , message): 
        # Send message to room group
        
        command = message.get("command" , None)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, # مقصد پیام
                {"type": "chat_message",
                "content": message["content"],
                "command" : (lambda command : "img" if (command == "img") else "new_message")(command),
                "__str__" : message["__str__"]
                }
        )

    # Receive message from room group
    def chat_message(self, event):
        #message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))