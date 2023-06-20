from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_certificate(request):
    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    # Create a canvas to draw on
    c = canvas.Canvas(response)

    # Add text to the PDF
    c.drawString(100, 700, "Certificate of Achievement")
    c.drawString(100, 650, "This is to certify that John Doe")
    c.drawString(100, 600, "has successfully completed the course")

    # Add an image to the PDF
    # image_path = f"{settings.STATIC_URL}images/verified.png"
    # print (image_path)
    c.drawInlineImage('verified.png', 100, 400, width=200, height=200)

    # Save the PDF and close the canvas
    c.save()

    return response