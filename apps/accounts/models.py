from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [('client','CLIENT'),
                    ('employee','EMPLOYEE'),
                    ('customer representative','CUSTOMER REPRESENTATIVE'),
                    ]
    # role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='client')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"