from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from backend.admin_mixins import RowActionsMixin
from .models import Product, Sale, SaleItem, Payment, Concept

@admin.register(Product)
class ProductAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)

class SaleItemInline(TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('id', 'date', 'buyer', 'get_total_display', 'print_button')
    list_filter = ('date',)
    inlines = [SaleItemInline]
    search_fields = ('buyer__username',)
    readonly_fields = ('get_total_display',)

    def get_total_display(self, obj):
        total = sum((item.quantity * item.price_at_sale) for item in obj.items.all() if item.price_at_sale)
        return f"{total:.2f}"
    get_total_display.short_description = 'Total (S/)'

    class Media:
        js = ('js/sale_price.js',)

    def print_button(self, obj):
        if obj.id:
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:billing_sale_receipt', args=[obj.id])
            return format_html('<a href="{}" target="_blank" style="color: #2563eb; font-weight: 600;"><span class="material-symbols-outlined" style="font-size: 20px; vertical-align: middle;">print</span> Imprimir</a>', url)
        return ""
    print_button.short_description = "Recibo"

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        custom_urls = [
            path('<int:sale_id>/receipt/', self.admin_site.admin_view(self.receipt_view), name='billing_sale_receipt'),
        ]
        return custom_urls + urls

    def receipt_view(self, request, sale_id):
        from django.shortcuts import get_object_or_404, render
        sale = get_object_or_404(Sale, id=sale_id)
        return render(request, 'admin/billing/sale_receipt.html', {'sale': sale})

@admin.register(Concept)
class ConceptAdmin(RowActionsMixin, ModelAdmin):
    list_display = ('name', 'default_amount')
    search_fields = ('name',)

from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render

@admin.register(Payment)
class PaymentAdmin(RowActionsMixin, ModelAdmin):
    autocomplete_fields = ('student', 'concept')
    list_display = ('receipt_number', 'student', 'concept', 'amount', 'is_paid', 'date_paid', 'print_button')
    list_filter = ('is_paid', 'concept', 'month', 'year')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'receipt_number')
    
    fieldsets = (
        ('Datos del Cliente', {
            'fields': (('student', 'receipt_number'),)
        }),
        ('Detalle de Cobro', {
            'fields': (('concept', 'amount'), ('month', 'year'))
        }),
        ('Estado de Pago', {
            'fields': (('is_paid', 'date_paid'),)
        }),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        from django.utils import timezone
        current_year = timezone.now().year
        last_payment = Payment.objects.order_by('id').last()
        next_id = last_payment.id + 1 if last_payment else 1
        initial['receipt_number'] = f"REC{current_year}-{next_id:05d}"
        return initial

    def print_button(self, obj):
        if obj.id:
            url = reverse('admin:billing_payment_receipt', args=[obj.id])
            return format_html('<a href="{}" target="_blank" style="color: #2563eb; font-weight: 600;"><span class="material-symbols-outlined" style="font-size: 20px; vertical-align: middle;">print</span> Imprimir</a>', url)
        return ""
    print_button.short_description = "Recibo"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:payment_id>/receipt/', self.admin_site.admin_view(self.receipt_view), name='billing_payment_receipt'),
        ]
        return custom_urls + urls

    def receipt_view(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, 'admin/billing/receipt.html', {'payment': payment})

    class Media:
        js = ('js/payment_auto_price.js',)
