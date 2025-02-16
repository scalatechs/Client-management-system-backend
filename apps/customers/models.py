from django.db import models
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.accounts.models import CustomUser


class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lead', 'Lead')
    ]

    # Basic Information
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region='NP')
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(
        upload_to='customer_images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'webp'])],
        blank=True,
        null=True
    )
    
    # Status & Interaction Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    last_interaction = models.DateField(auto_now_add=True)
    next_session = models.DateField(blank=True, null=True)
    
    # Financial Summary (Denormalized for quick access)
    total_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Address
    address = models.TextField(max_length=75)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_interaction']


class Interaction(models.Model):
    """Track customer communications (meetings, calls, emails)"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    attachment = models.FileField(
        upload_to='interaction_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.customer.name} - {self.date.strftime('%Y-%m-%d')}"


class CustomerProject(models.Model):
    """Link customers to projects (extendable for role-based access)"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_projects')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='client_projects')
    role = models.CharField(max_length=50, default='primary')  # e.g., "primary", "stakeholder"

    class Meta:
        unique_together = ('customer', 'project')