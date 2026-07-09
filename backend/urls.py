"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.http import JsonResponse
from django.views.generic import RedirectView
from billing.models import Concept, Product


def get_concept_price(request, concept_id):
    try:
        concept = Concept.objects.get(id=concept_id)
        return JsonResponse({'price': str(concept.default_amount)})
    except Concept.DoesNotExist:
        return JsonResponse({'price': ''}, status=404)


def get_product_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'price': str(product.price)})
    except Product.DoesNotExist:
        return JsonResponse({'price': ''}, status=404)


from django.conf import settings
from django.conf.urls.static import static
from django.core.management import call_command
from django.http import HttpResponse

def force_migrate(request):
    try:
        call_command('migrate', interactive=False)
        return HttpResponse("Migrated successfully")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('asistencia/', include('attendance.urls')),
    path('api/', include('api.urls')),
    path('api/concept-price/<int:concept_id>/', get_concept_price, name='get_concept_price'),
    path('api/product-price/<int:product_id>/', get_product_price, name='get_product_price'),
    path('force-migrate/', force_migrate),
]

from django.urls import re_path
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

admin.site.site_header = "Dojang Taekwondo Segma"
admin.site.site_title = "Portal Administrativo"
admin.site.index_title = "Panel de Control"
