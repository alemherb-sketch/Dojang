"""Helpers to auto-issue mobile-portal credentials for parents and students."""
import re
import secrets

from django.utils.text import slugify

# Unambiguous alphabet: no 0/O/1/l/I so credentials are easy to read/dictate.
_ALPHABET = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_password(length=8):
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def build_username(dni=None, first_name="", last_name="", fallback="usuario"):
    """Return a unique username, preferring the DNI (natural portal login in PE),
    otherwise a slug of the full name, otherwise the fallback."""
    from .models import User

    dni_digits = re.sub(r"\D", "", dni or "")
    if dni_digits:
        base = dni_digits
    else:
        base = slugify(f"{first_name} {last_name}").replace("-", ".").strip(".")
    base = base or fallback

    candidate = base
    counter = 1
    while User.objects.filter(username=candidate).exists():
        counter += 1
        candidate = f"{base}{counter}"
    return candidate
