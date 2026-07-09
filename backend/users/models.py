from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('INSTRUCTOR', 'Instructor'),
        ('PARENT', 'Padre/Apoderado'),
        ('STUDENT', 'Alumno'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Número de WhatsApp")
    qr_code = models.CharField(max_length=255, blank=True, null=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'role': 'PARENT'})

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
