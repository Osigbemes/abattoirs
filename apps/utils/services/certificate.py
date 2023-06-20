from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from django.conf import settings

def generate_certificate(request, abattoir):
    name = abattoir['abattoir'].name
    issuedBy = abattoir['abattoir']
    beefWeightInKg = abattoir['abattoir']
    animalSpecie = abattoir['animalSpecie']
    dispatchedTo = abattoir['dispatchedTo']
    
    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    # Set up the canvas
    c = canvas.Canvas(response, pagesize=letter)

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    text_style = styles['Normal']

    # Centered text
    centered_text = "Certificate of Trustworthiness"
    text_width = c.stringWidth(centered_text, "Helvetica", 24)
    page_width, page_height = letter
    x = (page_width - text_width) / 2
    y = (page_height)/2 + 280 

    # Draw centered text
    c.setFont("Helvetica", 24)
    c.setFillColor(colors.black)
    c.drawString(x, y, centered_text)

    c.setFont('Helvetica', 12)
    c.setFillColor(colors.black)
    c.drawString(0, 650, f"This is to certify that the abattoir named {name} has been recognized and certified as a trusted establishment in the field of meat processing and food safety. This certification is a testament to the abattoir's commitment to maintaining high standards of quality, hygiene, and ethical practices.")

    name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=18)
    name_text = '<b>John Doe</b>'
    name_paragraph = Paragraph(name_text, name_style)
    name_paragraph.wrapOn(c, 200, 200)
    name_paragraph.drawOn(c, 100, 620)
    
    c.drawString(100, 600, "has successfully completed the course")

    # Add an image to the PDF
    image_path = f"{settings.STATIC_URL}images/verified.png"
    image_path = image_path.lstrip('/')
    c.drawInlineImage(image_path, 250, 700, width=100, height=100)

    # Save the PDF and close the canvas
    c.showPage()
    c.save()

    return response
