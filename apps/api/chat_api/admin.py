from django.contrib import admin
from apps.api.chat_api.models import Conversation, EncryptedMessage

# Register your models here.
@admin.register(Conversation)
class ConversationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'representative', 'created_at']
    search_fields = ['client', 'representative']
    list_filter = ['client', 'representative']
    list_editable = ['client', 'representative']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['client', 'representative']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('client', 'representative')
    
@admin.register(EncryptedMessage)
class EncryptedMessageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'timestamp', 'encrypted_content']
    search_fields = ['conversation', 'sender']
    list_filter = ['conversation', 'sender']
    list_editable = ['conversation', 'sender',]
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['conversation', 'sender']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('conversation', 'sender')