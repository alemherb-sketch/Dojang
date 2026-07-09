from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("escanear/", views.scan_page, name="scan"),
    path("escanear/registrar/", views.scan_register, name="scan_register"),
]
