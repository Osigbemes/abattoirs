from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_certificate(certificate_data):
    doc = SimpleDocTemplate("certificate.pdf", pagesize=letter)

    # Add content to the PDF
    story = []
    styles = getSampleStyleSheet()
    
    # Add image to the PDF
    image_path = 'logos.logo.png'
    image = Image(image_path, width=2.5*inch, height=2.5*inch)
    story.append(image)
    
    # Add text to the PDF
    recipient_name = certificate_data['recipient_name']
    text = f"Certificate of Achievement\n\nThis is to certify that {recipient_name} has successfully completed the course."
    paragraph = Paragraph(text, styles["BodyText"])
    story.append(paragraph)

    doc.build(story)

    return "certificate.pdf"

def generate_certificate_for_abattoir(certificate_data):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Add content to the PDF
    story = []
    styles = getSampleStyleSheet()
    
    # Add image to the PDF
    image_path = 'logos.logo.png'
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
