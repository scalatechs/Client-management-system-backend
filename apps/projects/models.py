from django.db import models
from apps.accounts.models import CustomUser
from apps.customers.models import Customer
from django.core.validators import FileExtensionValidator
from apps.employes.models import Employee
from django.utils import timezone

class Project(models.Model):
    PRIORITY_CHOICES = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
    STATUS_CHOICES = [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')]

    # Core Fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_projects')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='client_projects')
    
    # Financial Fields
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Timeline Fields
    start_date = models.DateField()
    due_date = models.DateField()
    
    # Status Fields
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # File Upload
    document = models.FileField(
        upload_to='project_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx'])],
        blank=True,
        null=True
    )
    
    # Relationships
    employees = models.ManyToManyField('employes.Employee', through='employes.EmployeeProjectAssignment', related_name='assigned_projects')
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-due_date']


class Milestone(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    is_critical = models.BooleanField(default=False)
    file = models.FileField(
        upload_to="milestones/", 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])],
        blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completion_date:
            self.completion_date = timezone.now().date()
        super().save(*args, **kwargs)