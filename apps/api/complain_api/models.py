from django.db import models
from apps.projects.models import Project
from apps.accounts.models import CustomUser
from django.core.validators import FileExtensionValidator

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('payment', 'Payment'),
        ('design', 'Design'),
        ('delivery', 'Delivery'),
        ('other', 'Other')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='complaints')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    attachment = models.FileField(
        upload_to='complaint_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'png', 'jpg'])],
        blank=True,
        null=True
    )
    date_filed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.title}"

    class Meta:
        ordering = ['-date_filed']