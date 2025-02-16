from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Conversation, EncryptedMessage
from .serializers import MessageSerializer
from .permissions import IsConversationParticipant
from apps.accounts.models import CustomUser
from apps.api.chat_api.serializers import CustomUserSerializer
from django.db import models
from django.db.models import Q  


# ViewSet for Conversation
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = CustomUserSerializer  # Serializer for listing conversations
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter conversations based on whether the user is the client or representative.
        """
        return Conversation.objects.filter(
            models.Q(client=self.request.user) | models.Q(representative=self.request.user)
        )

    def perform_create(self, serializer):
        """
        Create a conversation and associate it with the current client and representative.
        """
        client = self.request.user
        representative = CustomUser.objects.get(id=self.request.data['representative_id'])
        serializer.save(client=client, representative=representative)


# ViewSet for EncryptedMessage
class MessageViewSet(viewsets.ModelViewSet):
    queryset = EncryptedMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsConversationParticipant]

    def get_queryset(self):
        """
        Return the list of messages for the current conversation.
        """
        conversation = Conversation.objects.get(id=self.kwargs['conversation_id'])
        return EncryptedMessage.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """
        Create a new message and associate it with the current conversation and sender.
        """
        conversation = Conversation.objects.get(id=self.kwargs['conversation_id'])
        serializer.save(conversation=conversation, sender=self.request.user)

    def get_serializer_class(self):
        """
        Dynamically return the serializer class based on the action
        """
        if self.action == 'list':
            return MessageSerializer
        return MessageSerializer  # Default serializer class for all actions
