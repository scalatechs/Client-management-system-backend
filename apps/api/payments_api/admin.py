from django.contrib import admin
from apps.api.payments_api.models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'amount']
    search_fields = ['amount']
    list_filter = ['amount']
    list_editable = ['amount']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['project']
    list_select_related = ()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('project')