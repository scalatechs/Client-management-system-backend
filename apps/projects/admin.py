from django.contrib import admin
from apps.projects.models import Project,Milestone

# Register your models here.
@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'start_date', 'due_date', 'status', 'manager', 'customer']
    search_fields = ['title', 'description', 'status']
    list_filter = ['status']
    list_editable = ['title', 'description', 'start_date', 'due_date', 'status']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['title', 'description', 'start_date', 'due_date', 'status']
    list_select_related = ('manager', 'customer')


@admin.register(Milestone)
class MilestoneModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'start_date', 'due_date', 'project']
    search_fields = ['title', 'description', 'project']
    list_filter = ['project']
    list_editable = ['title', 'description', 'start_date', 'due_date', 'project']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['title', 'description', 'start_date', 'due_date', 'project']
    list_select_related = ('project',)

