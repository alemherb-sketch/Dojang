from django.db import models
from django.conf import settings
from django.utils import timezone

class Product(models.Model):
    name = models.CharField('Nombre', max_length=200)
    description = models.TextField('Descripción', blank=True)
    price = models.DecimalField('Precio (S/)', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Stock', default=0)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.name} - S/ {self.price}"

class Sale(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Comprador')
    date = models.DateTimeField('Fecha', auto_now_add=True)
    total = models.DecimalField('Total (S/)', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-date']

    def __str__(self):
        return f"Venta #{self.id} - {self.date.strftime('%d/%m/%Y %H:%M')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Venta')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Producto')
    quantity = models.PositiveIntegerField('Cantidad', default=1)
    price_at_sale = models.DecimalField('Precio Unitario (S/)', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Eliminado'}"

    @property
    def subtotal(self):
        return self.quantity * self.price_at_sale

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F

@receiver([post_save, post_delete], sender=SaleItem)
def update_sale_total(sender, instance, **kwargs):
    sale = instance.sale
    if sale:
        # Calculate total
        total = sum(item.quantity * item.price_at_sale for item in sale.items.all() if item.price_at_sale)
        if sale.total != total:
            sale.total = total
            sale.save(update_fields=['total'])

MONTH_CHOICES = [
    ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'),
    ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
    ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'),
    ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),
]

class Concept(models.Model):
    name = models.CharField('Nombre del Concepto', max_length=200)
    default_amount = models.DecimalField('Monto Base (S/)', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Concepto de Pago'
        verbose_name_plural = 'Conceptos de Pago'

    def __str__(self):
        return self.name

class Payment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'}, verbose_name='Alumno')
    concept = models.ForeignKey(Concept, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Concepto')
    receipt_number = models.CharField('Nro. de Recibo', max_length=50, blank=True, null=True, help_text='Ej: F001-0000234')
    amount = models.DecimalField('Monto (S/)', max_digits=10, decimal_places=2)
    month = models.CharField('Mes', max_length=2, choices=MONTH_CHOICES, blank=True, null=True)
    year = models.IntegerField('Año', blank=True, null=True)
    is_paid = models.BooleanField('¿Pagado?', default=False)
    date_paid = models.DateTimeField('Fecha de Pago', default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = 'Pensión / Cobro'
        verbose_name_plural = 'Pensiones y Cobros'
        ordering = ['-date_paid', '-year', '-month']

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate receipt number: RECYYYY-XXXXX
            current_year = timezone.now().year
            last_payment = Payment.objects.order_by('id').last()
            next_id = last_payment.id + 1 if last_payment else 1
            self.receipt_number = f"REC{current_year}-{next_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        concept_name = self.concept.name if self.concept else "Pensión"
        return f"{concept_name} - {self.student}"
