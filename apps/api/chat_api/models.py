from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
from apps.accounts.models import CustomUser



class Conversation(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                              related_name='client_conversations',
                              limit_choices_to={'role': 'client'})
    representative = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                      related_name='rep_conversations',
                                      limit_choices_to={'role': 'customer representative'})
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'representative', 'project')


    def __str__(self):
        return f"Conversation between {self.client} and {self.representative}"

class EncryptedMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    encrypted_content = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def set_content(self, raw_content):
        """Encrypts the message before saving"""
        try:
            self.encrypted_content = settings.CIPHER_SUITE.encrypt(raw_content.encode())
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")


    def get_content(self):
        """Decrypts and returns the original message securely"""
        try:
            return settings.CIPHER_SUITE.decrypt(self.encrypted_content).decode()
        except Exception as e:
            return "Decryption Error: Invalid Key or Corrupted Data"

    class Meta:
        ordering = ['-timestamp']