from django.contrib import admin
from apps.employes.models import Employee, EmployeeProjectAssignment, Contract

# Register your models here.
@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','get_email', 'phone', 'address']
    search_fields = ['user__email', 'phone', 'address']
    list_filter = ['user']
    list_editable = ['phone', 'address']
    list_per_page = 10
    list_display_links = ['id']
    # list_select_related = ['user', 'email', 'phone', 'address']
    list_select_related = ('user',)

    def get_email(self, obj):
        return obj.user.email  # Access email from related CustomUser
    get_email.short_description = 'Email'  # Set column name in Django Admin
    get_email.admin_order_field = 'user__email'  # Allow sorting by email


    
@admin.register(EmployeeProjectAssignment)
class EmployeeProjectAssignmentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'project', 'role', 'start_date', 'end_date', 'status']
    search_fields = ['employee__user__email', 'project__title', 'role', 'status']
    list_filter = ['employee', 'project', 'role', 'status']
    list_editable = ['role', 'start_date', 'end_date', 'status']
    list_per_page = 10
    list_display_links = ['id']
    list_select_related = ['employee', 'project', 'role', 'start_date', 'end_date', 'status']
    list_select_related = ('employee', 'project')

    # def get_employee_name(self, obj):
    #     return obj.employee.user.get_username()
@admin.register(Contract)
class ContractModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'start_date', 'end_date']
    search_fields = ['employee__user__email', 'project__title']
    list_filter = ['employee', 'start_date', 'end_date']
    list_editable = ['start_date', 'end_date']
    list_per_page = 10
    list_display_links = ['id']
    # list_select_related = ['employee', 'start_date', 'end_date', 'salary', 'terms']
    list_select_related = ('employee',)