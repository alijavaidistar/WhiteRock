import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black
from django.conf import settings
from .models import Request

def generate_request_pdf(request_id, approved_by=None):
    """ Generate a clean, professional PDF for the request including approval details. """
    req = Request.objects.get(id=request_id)  # ✅ Fetch latest request status

    # ✅ Debugging: Print request details
    print(f"Generating PDF for Request ID: {req.id}")
    print(f"Request Status: {req.status}")
    print(f"Approved By (Received in Function): {approved_by if approved_by else 'N/A'}")

    # Ensure req.data is a dictionary
    req_data = json.loads(req.data) if isinstance(req.data, str) else req.data or {}

    # Define the PDF file path
    pdf_filename = f"request_{req.id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, "request_pdfs", pdf_filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create the PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)

     # ✅ Add Logo on Top of Form
    logo_path = r"C:\Users\ali\Documents\GitHub\WhiteRock\uhlogo1.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, x=240, y=760, width=120, height=50, preserveAspectRatio=True, mask='auto')
    else:
        print(f"⚠️ Logo not found at: {logo_path}")

    # ✅ University Header
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(red)  # ✅ University of Houston in red
    c.drawCentredString(300, 770, "University of Houston")




    c.setFillColor(black)  # ✅ Reset color for black text
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 750, "Office of the Registrar")

    c.line(50, 740, 550, 740)  # ✅ Line separator

    # ✅ Request Form Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 720, f"{req.form_name.upper()}")

    # ✅ Student Information Section
    y_position = 680
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "STUDENT INFORMATION")
    c.setFont("Helvetica", 12)

    y_position -= 20
    c.setFont("Helvetica-Bold", 12)  # ✅ Bold questions
    c.drawString(50, y_position, "Student Name:")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_position, f"{req.user.get_full_name()}")

    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Email:")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_position, f"{req.user.email}")

    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Request Type:")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_position, f"{req.form_name}")

    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Submitted On:")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_position, f"{req.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # ✅ Request Details Section
    y_position -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "REQUEST DETAILS")
    
    y_position -= 20
    for key, value in req_data.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"{key}:")
        c.setFont("Helvetica", 12)
        c.drawString(200, y_position, f"{value}")
        y_position -= 20

    # ✅ Approval Status
    y_position -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "APPROVAL STATUS")

    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Request Status:")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_position, f"{req.status.capitalize()}")

    # ✅ Show comments if returned
    if req.status == "returned" and req.comments:
        y_position -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "ADMIN COMMENTS")
        
        y_position -= 20
        c.setFont("Helvetica", 12)
        c.drawString(50, y_position, f"{req.comments}")

    # ✅ Admin Signature Section
    y_position -= 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "APPROVED BY")
    
    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    if approved_by:
        c.drawString(50, y_position, "Admin Name:")
        c.setFont("Helvetica", 12)
        c.drawString(200, y_position, f"{approved_by}")  # ✅ Always shows a valid name
    else:
        c.drawString(50, y_position, "Approved By: UNKNOWN")  # ✅ If still missing, show 'UNKNOWN'

    # ✅ Footer for official use
    y_position -= 60
    c.line(50, y_position, 550, y_position)

    c.setFont("Helvetica", 10)
    c.drawCentredString(300, y_position - 20, "This document is issued by the University of Houston for official use only.")

    c.save()

    return pdf_filename  # ✅ Return the filename for storing in DB
