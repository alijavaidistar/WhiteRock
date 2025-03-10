import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings
from .models import Request

def generate_request_pdf(request_id):
    """ Generate a PDF for the approved withdrawal request. """
    req = Request.objects.get(id=request_id)

    # Debugging: Check the type of req.data
    print("DEBUG: req.data =", req.data)
    print("DEBUG: Type of req.data =", type(req.data))

    # Ensure req.data is a dictionary
    if isinstance(req.data, str):
        try:
            req_data = json.loads(req.data)  # Convert string to dictionary
        except json.JSONDecodeError:
            print("ERROR: req.data is not valid JSON! Using empty dictionary.")
            req_data = {}  # Default to an empty dictionary
    elif isinstance(req.data, dict):
        req_data = req.data  # It's already a dictionary
    else:
        print("WARNING: req.data is an unexpected type! Using empty dictionary.")
        req_data = {}  # Default to an empty dictionary

    print("DEBUG: req_data (after conversion) =", req_data)
    print("DEBUG: Type of req_data =", type(req_data))

    # Define the PDF file path
    pdf_filename = f"withdrawal_request_{req.id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, "request_pdfs", pdf_filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create the PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Title
    c.drawString(200, 750, "University Term Withdrawal Request")
    c.line(50, 740, 550, 740)

    # Student Information (use .get() to avoid crashes)
    c.drawString(50, 710, f"Student Name: {req.user.get_full_name()}")
    c.drawString(50, 690, f"myUH ID: {req_data.get('myuh_id', 'N/A')}")
    c.drawString(50, 670, f"Phone: {req_data.get('phone', 'N/A')}")
    c.drawString(50, 650, f"Email: {req.user.email}")
    c.drawString(50, 630, f"Program/Plan: {req_data.get('program_plan', 'N/A')}")
    c.drawString(50, 610, f"Academic Career: {req_data.get('academic_career', 'N/A')}")
    c.drawString(50, 590, f"Withdrawal Term: {req_data.get('withdrawal_term', 'N/A')}")

    # Approval Information
    c.drawString(50, 550, f"Request Status: {req.status}")
    c.drawString(50, 530, f"Approved By: Admin")

    # Footer
    c.line(50, 500, 550, 500)
    c.drawString(50, 480, "This is an official document for record-keeping purposes.")

    c.save()
    
    return pdf_filename  # Return filename for saving in DB
