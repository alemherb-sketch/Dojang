from django.db import models
from django.conf import settings

class Grade(models.Model):
    name = models.CharField('Nombre', max_length=100, help_text="Nombre del grado o cinturón")
    color = models.CharField('Color', max_length=50, blank=True)
    description = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Grado / Cinturón'
        verbose_name_plural = 'Grados / Cinturones'

    def __str__(self):
        return self.name

class Activity(models.Model):
    title = models.CharField('Título', max_length=200, help_text="Título del anuncio o actividad")
    content = models.TextField('Contenido', help_text="Detalle de la actividad")
    date_posted = models.DateTimeField('Fecha de Publicación', auto_now_add=True)
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Actividad / Aviso'
        verbose_name_plural = 'Actividades / Avisos'
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

class Section(models.Model):
    name = models.CharField('Nombre', max_length=100, help_text="Nombre del grupo o sección (Ej. Infantiles Martes/Jueves)")
    schedule = models.CharField('Horario', max_length=200, help_text="Ej: Lunes y Miércoles 4:00pm - 5:30pm")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'INSTRUCTOR'},
        related_name='sections',
        verbose_name='Instructor'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'STUDENT'},
        related_name='enrolled_sections',
        blank=True,
        verbose_name='Alumnos'
    )

    class Meta:
        verbose_name = 'Grupo de Alumnos'
        verbose_name_plural = 'Grupos de Alumnos'

    def __str__(self):
        return self.name
