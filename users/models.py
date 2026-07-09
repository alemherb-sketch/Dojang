import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


def generate_qr_token():
    return uuid.uuid4().hex


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('INSTRUCTOR', 'Instructor'),
        ('PARENT', 'Padre/Apoderado'),
        ('STUDENT', 'Alumno'),
    )
    role = models.CharField('Rol', max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField('Nro. WhatsApp', max_length=20, blank=True, null=True, help_text="Número de WhatsApp con código de país (+51)")
    qr_code = models.CharField('Código QR', max_length=255, blank=True, null=True, unique=True)
    dni = models.CharField('DNI', max_length=15, blank=True, null=True)
    birth_date = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    address = models.CharField('Dirección', max_length=255, blank=True, null=True)
    blood_type = models.CharField('Grupo Sanguíneo', max_length=10, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'role': 'PARENT'}, verbose_name='Apoderado')
    portal_password = models.CharField('Contraseña del Portal (Visible)', max_length=128, blank=True, null=True, help_text="Contraseña en texto plano para fines administrativos.")

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def save(self, *args, **kwargs):
        # Every student needs a unique QR token to be scanned for attendance.
        if self.role == 'STUDENT' and not self.qr_code:
            self.qr_code = generate_qr_token()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='STUDENT')


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'STUDENT'
        super().save(*args, **kwargs)


class ParentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='PARENT')


class Parent(User):
    objects = ParentManager()

    class Meta:
        proxy = True
        verbose_name = 'Apoderado'
        verbose_name_plural = 'Apoderados'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'PARENT'
        super().save(*args, **kwargs)


class InstructorManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='INSTRUCTOR')


class Instructor(User):
    objects = InstructorManager()

    class Meta:
        proxy = True
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructores'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'INSTRUCTOR'
        super().save(*args, **kwargs)
