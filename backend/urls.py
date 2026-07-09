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
from billing.models import Concept

def get_concept_price(request, concept_id):
    try:
        concept = Concept.objects.get(id=concept_id)
        return JsonResponse({'price': str(concept.default_amount)})
    except Concept.DoesNotExist:
        return JsonResponse({'price': ''}, status=404)

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('asistencia/', include('attendance.urls')),
    path('api/', include('api.urls')),
    path('api/concept-price/<int:concept_id>/', get_concept_price, name='get_concept_price'),
]

admin.site.site_header = "Dojang Taekwondo Segma"
admin.site.site_title = "Portal Administrativo"
admin.site.index_title = "Panel de Control"
