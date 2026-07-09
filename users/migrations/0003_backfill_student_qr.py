import uuid

from django.db import migrations
from django.db.models import Q


def backfill_qr(apps, schema_editor):
    User = apps.get_model("users", "User")
    students = User.objects.filter(role="STUDENT").filter(
        Q(qr_code__isnull=True) | Q(qr_code="")
    )
    for user in students:
        user.qr_code = uuid.uuid4().hex
        user.save(update_fields=["qr_code"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_options_alter_user_parent_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_qr, migrations.RunPython.noop),
    ]
