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
    title = models.CharField('Título', max_length=200)
    content = models.TextField('Contenido')
    image = models.ImageField('Imagen (opcional)', upload_to='activities/', null=True, blank=True)
    image_base64 = models.TextField('Imagen Base64', blank=True, null=True, editable=False)
    date_posted = models.DateTimeField('Fecha de Publicación', auto_now_add=True)
    is_active = models.BooleanField('Activo', default=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image_base64:
            try:
                import base64
                self.image.file.seek(0)
                file_data = self.image.file.read()
                self.image_base64 = "data:image/png;base64," + base64.b64encode(file_data).decode('utf-8')
            except Exception:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
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
