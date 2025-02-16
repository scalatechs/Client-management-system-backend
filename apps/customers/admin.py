from django.contrib import admin
from apps.customers.models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'address']
    search_fields = ['name', 'email', 'phone', 'address']
    list_filter = ['name']
    list_editable = ['name', 'email', 'phone', 'address']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['name', 'email', 'phone', 'address']
    list_select_related = ()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('interactions') 