from rest_framework import serializers
from .models import Conversation, EncryptedMessage
from apps.api.accounnts_api.serializers import CustomUserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)  # Include sender details
    content = serializers.CharField(write_only=True, required=False)  # Make content optional
    decrypted_content = serializers.SerializerMethodField()  # Readable decrypted content

    class Meta:
        model = EncryptedMessage
        fields = ['id', 'sender', 'decrypted_content', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'sender', 'timestamp', 'decrypted_content', 'is_read']

    def get_decrypted_content(self, obj):
        """Decrypt message content before returning"""
        return obj.get_content()

    def create(self, validated_data):
        """Encrypts and saves the message"""
        content = validated_data.pop('content', None)  # Default to None if missing

        # Ensure 'conversation' exists in validated_data
        conversation = validated_data.get('conversation')
        if not conversation:
            raise serializers.ValidationError("Conversation is required to send a message.")

        # Create and encrypt the message
        message = EncryptedMessage(**validated_data)
        if content:
            message.set_content(content)  # Encrypt content
        message.save()
        return message
