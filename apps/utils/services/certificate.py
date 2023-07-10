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
from reportlab.lib.units import inch
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing

def generate_certificate(request, abattoir):
    name = abattoir['abattoir'].name
    issuedBy = abattoir['issuedBy'].firstname + ' ' + abattoir['issuedBy'].lastname
    beefWeightInKg = abattoir['beefWeightInKg']
    animalSpecie = abattoir['animalSpecie']
    dispatchedTo = abattoir['dispatchedTo']
    code = abattoir['code']
    date_issued = abattoir['date_issued']
    
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
    centered_text = "Abattoir Certificate"
    text_width = c.stringWidth(centered_text, "Helvetica", 24)
    page_width, page_height = letter
    x = (page_width - text_width) / 2
    y = (page_height)/2 + 280 

    # Draw centered text
    c.setFont("Helvetica", 24)
    c.setFillColor(colors.black)
    c.drawString(x, y, centered_text)
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(25, 740, f"{code}")
    
    abattoir_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15, spaceAfter=20)
    abattoir_name_text = f'Abattoir Name: <b>{name}</b>'
    abattoir_name_paragraph = Paragraph(abattoir_name_text, abattoir_name_style)
    abattoir_name_paragraph.wrapOn(c, 200, 200)
    abattoir_name_paragraph.drawOn(c, 100, 620)
    
    issuedBy_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15)
    issuedBy_name_text = f'Issued By : <b>{issuedBy}</b>'
    issuedBy_name_paragraph = Paragraph(issuedBy_name_text, issuedBy_name_style)
    issuedBy_name_paragraph.wrapOn(c, 200, 200)
    issuedBy_name_paragraph.drawOn(c, 100, 580)
    
    beefWeightInKg_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15)
    beefWeightInKg_name_text = f'Beef Weight In Kg: <b>{beefWeightInKg}</b>'
    beefWeightInKg_name_paragraph = Paragraph(beefWeightInKg_name_text, beefWeightInKg_name_style)
    beefWeightInKg_name_paragraph.wrapOn(c, 200, 200)
    beefWeightInKg_name_paragraph.drawOn(c, 100, 540)
    
    animalSpecie_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15)
    animalSpecie_name_text = f'Animal Specie: <b>{animalSpecie}</b>'
    animalSpecie_name_paragraph = Paragraph(animalSpecie_name_text, animalSpecie_name_style)
    animalSpecie_name_paragraph.wrapOn(c, 200, 200)
    animalSpecie_name_paragraph.drawOn(c, 100, 500)
    
    dispatchedTo_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15)
    dispatchedTo_name_text = f'Dispatched To: <b>{dispatchedTo}</b>'
    dispatchedTo_name_paragraph = Paragraph(dispatchedTo_name_text, dispatchedTo_name_style)
    dispatchedTo_name_paragraph.wrapOn(c, 200, 200)
    dispatchedTo_name_paragraph.drawOn(c, 100, 460)
    
    date_issued_name_style = ParagraphStyle(name='NameStyle', parent=text_style, fontSize=15)
    date_issued_name_text = f'Certificate Issue Date: <b>{date_issued.strftime("%B %d, %Y")}</b>'
    date_issued_name_paragraph = Paragraph(date_issued_name_text, date_issued_name_style)
    date_issued_name_paragraph.wrapOn(c, 200, 200)
    date_issued_name_paragraph.drawOn(c, 100, 415)

    # Add an image to the PDF
    image_path = f"{settings.STATIC_URL}images/verified.png"
    image_path = image_path.lstrip('/')
    c.drawInlineImage(image_path, 250, 700, width=100, height=100)
    
    # Create a QR code widget
    qr_code_value = "http://localhost:8000/certificate/issue/1/get_certificate"  # Replace with the actual URL or data for the QR code
    qr_code = QrCodeWidget(qr_code_value)

    # Set the QR code properties
    qr_code.barWidth = 1.2 * inch
    qr_code.barHeight = 1.2 * inch

    # Create a Drawing object to hold the QR code
    qr_code_drawing = Drawing(25, 25)
    qr_code_drawing.add(qr_code)

    # Draw the QR code on the canvas
    qr_code_drawing.drawOn(c, 500, 700)


    # Save the PDF and close the canvas
    c.showPage()
    c.save()

    return response
