from django.db import models
from django.conf import settings
from academy.models import Section

class Attendance(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='attendances',
        verbose_name='Alumno'
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True, verbose_name='Sección')
    date = models.DateField('Fecha', auto_now_add=True)
    time = models.TimeField('Hora', auto_now_add=True)
    status = models.CharField('Estado', max_length=20, choices=[
        ('PRESENT', 'Presente'),
        ('LATE', 'Tardanza'),
        ('ABSENT', 'Ausente')
    ], default='PRESENT')

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
