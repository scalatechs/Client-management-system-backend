from django.contrib import admin
from apps.api.complain_api.models import Complaint

# Register your models here.
@admin.register(Complaint)
class ComplaintModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'user', 'title', 'category', 'priority', 'status', 'date_filed']
    search_fields = ['title', 'category', 'priority', 'status']
    list_filter = ['title', 'category', 'priority', 'status']
    list_editable = ['title', 'category', 'priority', 'status']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['project', 'user']
    list_select_related = ()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('project', 'user')