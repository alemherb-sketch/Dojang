"""Render a student's ``qr_code`` token as a self-contained SVG.

Uses the pure-Python ``qrcode`` package to build the module matrix (no Pillow
needed) and emits an inline SVG string. Kept dependency-light so the QR can be
embedded directly in admin pages and print sheets without any external asset.
"""
import qrcode


def qr_svg(data, module_px=6, border=2, dark="#0f172a", light="#ffffff"):
    """Return an SVG markup string encoding ``data`` as a QR code.

    ``module_px`` is the rendered pixel size of one QR module; ``border`` is the
    quiet-zone width in modules (QR spec recommends >= 4, but 2 is fine on
    screen). Dark modules are drawn as a single ``<path>`` for compactness.
    """
    if not data:
        return ""

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()  # includes the quiet-zone border
    dim = len(matrix)

    segments = []
    for r, row in enumerate(matrix):
        for c, filled in enumerate(row):
            if filled:
                segments.append(f"M{c} {r}h1v1h-1z")
    path = "".join(segments)

    size = dim * module_px
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {dim} {dim}" '
        f'width="{size}" height="{size}" shape-rendering="crispEdges" '
        f'role="img" aria-label="Código QR">'
        f'<rect width="{dim}" height="{dim}" fill="{light}"/>'
        f'<path d="{path}" fill="{dark}"/>'
        f"</svg>"
    )
