import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings
from .models import Request

def generate_request_pdf(request_id, admin_signature=None):
    """ Generate a signed PDF for the approved request. """
    req = Request.objects.get(id=request_id)

    # Ensure req.data is a dictionary
    try:
        req_data = json.loads(req.data) if req.data else {}
    except json.JSONDecodeError:
        req_data = {}

    # Define the PDF file path
    pdf_filename = f"request_{req.id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, "request_pdfs", pdf_filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create the PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Title
    c.drawString(200, 750, "Request Approval Form")
    c.line(50, 740, 550, 740)

    # Student Information
    c.drawString(50, 710, f"Student Name: {req.user.get_full_name()}")
    c.drawString(50, 690, f"Email: {req.user.email}")
    c.drawString(50, 670, f"Request Type: {req.form_name}")
    c.drawString(50, 650, f"Submitted On: {req.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Draw Request Data
    y_position = 620
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Request Details:")
    c.setFont("Helvetica", 12)
    
    y_position -= 20
    for key, value in req_data.items():
        c.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    # Approval Status
    c.drawString(50, y_position - 10, f"Request Status: {req.status}")
    
    # Signature Section
    y_position -= 50
    if admin_signature:
        c.drawString(50, y_position, "Admin Approval Signature:")
        c.drawImage(admin_signature, 250, y_position - 20, width=100, height=50)

    # Footer
    c.line(50, y_position - 50, 550, y_position - 50)
    c.drawString(50, y_position - 70, "This is an official document for record-keeping purposes.")

    c.save()

    return pdf_filename  # Return the filename for storing in DB
