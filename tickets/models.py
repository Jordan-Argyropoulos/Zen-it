from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES = [('new','Nouveau'), ('open','En cours'), ('resolved','Résolu')]
    PRIORITY_CHOICES = [('low','Basse'), ('medium','Moyenne'), ('high','Haute'), ('urgent','Urgente')]
    CATEGORY_CHOICES = [('hardware','Matériel'), ('software','Logiciel'), ('network','Réseau'), ('email','Email'), ('other','Autre')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_technician': True})
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ai_first_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
