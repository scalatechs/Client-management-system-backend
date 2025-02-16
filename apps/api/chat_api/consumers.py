import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.accounts.models import CustomUser  # Import your user model
from .models import Conversation, EncryptedMessage

class SecureChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Authenticate user and establish WebSocket connection """
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.user = await self.authenticate_user()

        if self.user.is_anonymous:
            await self.close()  # Reject connection if unauthorized
            return

        if await self.validate_conversation_access():
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """ Remove user from chat group when disconnected """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ Receive and broadcast chat messages securely """
        data = json.loads(text_data)
        message = await self.save_message(data.get('content', ''))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'sender_id': self.user.id,
                'content': message.get_content(),
                'timestamp': str(message.timestamp)
            }
        )

    async def chat_message(self, event):
        """ Send messages to WebSocket clients """
        await self.send(text_data=json.dumps(event))

    @property
    def room_group_name(self):
        """ Generate unique group name for the chat room """
        return f"chat_{self.conversation_id}"

    @database_sync_to_async
    def authenticate_user(self):
        """ Authenticate user using JWT from headers (Secure method) """
        try:
            headers = dict(self.scope["headers"])
            token = headers.get(b'authorization', b'').decode()
            if not token.startswith("Bearer "):
                return AnonymousUser()
            
            jwt_token = token.split("Bearer ")[1]
            decoded_token = AccessToken(jwt_token)
            user_id = decoded_token["user_id"]
            return CustomUser.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()

    @database_sync_to_async
    def validate_conversation_access(self):
        """ Check if user is part of the conversation """
        if self.user.is_anonymous:
            return False  # Reject anonymous users

        return Conversation.objects.filter(
            Q(client=self.user) | Q(representative=self.user)
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        """ Save encrypted message in the database """
        conversation = get_object_or_404(Conversation, id=self.conversation_id)
        message = EncryptedMessage(
            conversation=conversation,
            sender=self.user
        )
        message.set_content(content)
        message.save()
        return message
