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
import os

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


def health(request):
    """Temporary deploy diagnostic. Reports DB backend + connectivity without
    leaking secrets. Safe to remove once login works."""
    from django.conf import settings
    from django.contrib.sessions.backends.db import SessionStore

    info = {
        'db_engine': settings.DATABASES['default'].get('ENGINE'),
        'db_name': str(settings.DATABASES['default'].get('NAME'))[:40],
        'DATABASE_URL_env_set': bool(os.environ.get('DATABASE_URL')),
        'DEBUG': settings.DEBUG,
    }
    try:
        from users.models import User
        info['db_connect_ok'] = True
        info['user_count'] = User.objects.count()
        info['superuser_exists'] = User.objects.filter(is_superuser=True).exists()
    except Exception as exc:
        info['db_connect_ok'] = False
        info['db_error'] = f'{type(exc).__name__}: {exc}'[:200]
    try:
        s = SessionStore()
        s['ping'] = 1
        s.create()
        s.delete()
        info['session_write_ok'] = True
    except Exception as exc:
        info['session_write_ok'] = False
        info['session_error'] = f'{type(exc).__name__}: {exc}'[:200]
    return JsonResponse(info)

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
    path('asistencia/', include('attendance.urls')),
    path('api/', include('api.urls')),
    path('api/concept-price/<int:concept_id>/', get_concept_price, name='get_concept_price'),
]

admin.site.site_header = "Dojang Taekwondo Segma"
admin.site.site_title = "Portal Administrativo"
admin.site.index_title = "Panel de Control"
