import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def generate_qr(registration):

    qr = qrcode.make(registration.ticket_id)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    registration.qr_code.save(
        f"{registration.ticket_id}.png",
        ContentFile(buffer.getvalue()),
        save=True
    )