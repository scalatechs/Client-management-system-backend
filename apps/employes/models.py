from django.db import models
from apps.accounts.models import CustomUser
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    phone = PhoneNumberField(region='NP')
    address = models.TextField(max_length=50)
    position = models.CharField(max_length=100) 
    date_joined = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    
    # Relationships
    projects = models.ManyToManyField('projects.Project', through='EmployeeProjectAssignment', related_name='team_members')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Contract(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='contract_details')
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.TextField()

class EmployeeProjectAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_assignments')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='assignments')
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed')
    ])

    def __str__(self):
        return f"{self.employee.user} - {self.project.title}"