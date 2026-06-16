from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('B2C', 'Particulier'),
        ('B2B', 'Entreprise'),
        ('TECH', 'Technicien'),
        ('ADMIN', 'Administrateur'),
    ]
    
    user_type = models.CharField(max_length=4, choices=USER_TYPE_CHOICES)
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_technician = models.BooleanField(default=False)
    
    def is_b2b_client(self):
        return self.user_type == 'B2B'
    
    def is_b2c_client(self):
        return self.user_type == 'B2C'
