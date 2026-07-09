from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from academy.models import Section
from users.models import User

from .models import Attendance


def _student_label(student):
    full = student.get_full_name().strip()
    return full or student.username


@staff_member_required
def scan_page(request):
    """Attendance scanning console (USB/keyboard-wedge scanner or device camera)."""
    context = {
        **admin.site.each_context(request),
        "title": "Registrar Asistencia",
        "sections": Section.objects.all().order_by("name"),
        "status_choices": Attendance._meta.get_field("status").choices,
        "recent": [
            {
                "student": _student_label(a.student),
                "section": a.section.name if a.section else "—",
                "time": a.time.strftime("%H:%M"),
                "status": a.get_status_display(),
            }
            for a in Attendance.objects.select_related("student", "section").filter(
                date=timezone.localdate()
            )[:20]
        ],
    }
    return render(request, "admin/attendance/scan.html", context)


@staff_member_required
@require_POST
def scan_register(request):
    """Register attendance from a scanned QR token. Date/time are captured now."""
    code = (request.POST.get("code") or "").strip()
    section_id = request.POST.get("section") or None
    status = request.POST.get("status") or "PRESENT"

    if not code:
        return JsonResponse(
            {"ok": False, "message": "No se recibió ningún código."}, status=400
        )

    try:
        student = User.objects.get(qr_code=code, role="STUDENT")
    except User.DoesNotExist:
        return JsonResponse(
            {
                "ok": False,
                "message": "QR no reconocido. El alumno no existe o el código es inválido.",
            },
            status=404,
        )

    today = timezone.localdate()
    duplicate_qs = Attendance.objects.filter(student=student, date=today)
    if section_id:
        duplicate_qs = duplicate_qs.filter(section_id=section_id)

    existing = duplicate_qs.first()
    if existing:
        return JsonResponse(
            {
                "ok": False,
                "duplicate": True,
                "student": _student_label(student),
                "time": existing.time.strftime("%H:%M"),
                "message": f"{_student_label(student)} ya registró asistencia hoy a las {existing.time.strftime('%H:%M')}.",
            }
        )

    attendance = Attendance.objects.create(
        student=student,
        section_id=section_id or None,
        status=status,
    )

    return JsonResponse(
        {
            "ok": True,
            "student": _student_label(student),
            "section": attendance.section.name if attendance.section else "—",
            "status": attendance.get_status_display(),
            "date": attendance.date.strftime("%d/%m/%Y"),
            "time": attendance.time.strftime("%H:%M:%S"),
            "message": f"Asistencia registrada para {_student_label(student)}.",
        }
    )
