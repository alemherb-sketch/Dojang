"""Idempotently ensure an admin superuser exists (for automated deploys).

Reads DJANGO_SUPERUSER_USERNAME / _PASSWORD / _EMAIL from the environment.
Safe to run on every deploy: it only creates the user when missing and never
overwrites an existing password unless DJANGO_SUPERUSER_FORCE_RESET=True.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create/ensure a superuser from environment variables."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD no está definido; se omite la creación del superusuario."
            ))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.role = "ADMIN"
        if created or os.environ.get("DJANGO_SUPERUSER_FORCE_RESET") == "True":
            user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Superusuario '{username}' {'creado' if created else 'verificado'}."
        ))
