from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas

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
    c.drawInlineImage('logo.png', 100, 400, width=200, height=200)

    # Save the PDF and close the canvas
    c.save()

    return response


# def generate_certificate(certificate_data):
#     doc = SimpleDocTemplate("certificate.pdf", pagesize=letter)

#     # Add content to the PDF
#     story = []
#     styles = getSampleStyleSheet()
    
#     # Add image to the PDF
#     # image_path = os.path.join(static_dir, 'images', 'logo.png')
#     image_path = 'logo.png'
#     image = Image(image_path, width=2.5*inch, height=2.5*inch)
#     story.append(image)
    
#     # Add text to the PDF
#     recipient_name = certificate_data['recipient_name']
#     text = f"Certificate of Achievement\n\nThis is to certify that {recipient_name} has successfully completed the course."
#     paragraph = Paragraph(text, styles["BodyText"])
#     story.append(paragraph)

#     doc.build(story)

#     return "certificate.pdf"

def generate_certificate_for_abattoir(certificate_data):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Add content to the PDF
    story = []
    styles = getSampleStyleSheet()
    
    # Add image to the PDF
    image_path = 'logo.png'
    image = Image(image_path, width=2.5*inch, height=2.5*inch)
    story.append(image)
    
    # Add text to the PDF
    recipient_name = certificate_data['recipient_name']
    text = f"Certificate of Achievement\n\nThis is to certify that {recipient_name} has successfully completed the course."
    paragraph = Paragraph(text, styles["BodyText"])
    story.append(paragraph)


    doc.build(story)

    pdf_buffer.seek(0)
    return pdf_buffer

generate_certificate({'recipient_name':'osigbemes'})

# def find_missing_number(num, *array):
#     if num in array:
#         return num
#     print (num in array)
#     print ('number not found')
    
# find_missing_number(3, ([1,2,3,4,5,6]))