from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Request
from .forms import RequestForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
import os
from django.conf import settings
import json
from django.core.files.uploadedfile import InMemoryUploadedFile

from .utils import generate_request_pdf

@login_required
def submit_request(request):
    form_name = request.GET.get('form_name', '')

    if form_name == "Veteran Benefits":
        form_name = "Veteran Educational Benefits"

    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.status = 'pending'

            # ✅ Exclude file uploads from JSON storage
            json_ready_data = {}
            for key, value in form.cleaned_data.items():
                if not isinstance(value, InMemoryUploadedFile):  # ✅ Ignore file uploads
                    json_ready_data[key] = value

            # ✅ Store only JSON-serializable data
            new_request.data = json.dumps(json_ready_data)

            print("Storing Data:", new_request.data)  # ✅ Debug before saving

            # ✅ Handle file uploads separately
            if 'signature' in request.FILES:
                new_request.signature = request.FILES['signature']  # ✅ Store file in DB

            new_request.save()
            return redirect('request_list')

    else:
        form = RequestForm(initial={'form_name': form_name}, user=request.user)

    return render(request, 'approval_system/submit_request.html', {'form': form, 'form_name': form_name})



@login_required
def request_list(request):
    requests = Request.objects.filter(user=request.user)  # Get only this user's requests
    return render(request, 'approval_system/request_list.html', {'requests': requests})






# Ensure only admin users can access this page
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_requests(request):
    requests = Request.objects.all()  # Fetch all requests
    return render(request, 'approval_system/admin_requests.html', {'requests': requests})


    req = Request.objects.get(id=request_id)
    req.status = 'approved'
    req.save()
    return redirect('admin_requests')



@login_required
def download_pdf(request, request_id):
    req = Request.objects.get(id=request_id)

    # Ensure the PDF file exists
    if not req.pdf_file:
        return redirect('request_list')

    # ✅ Convert FieldFile to string path
    pdf_path = os.path.join(settings.MEDIA_ROOT, str(req.pdf_file))  # ✅ Convert to string

    # ✅ Check if file exists before returning
    if not os.path.exists(pdf_path):
        return redirect('request_list')

    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')



@login_required
@user_passes_test(is_admin)
def review_request(request, request_id):
    req = Request.objects.get(id=request_id)

    # Convert JSON `data` into a Python dictionary
    form_data = json.loads(req.data) if req.data else {}

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            # ✅ First, update the request status and save it
            req.status = "approved"
            req.save()  # ✅ Save to ensure the correct status before PDF generation

            # ✅ Get admin's full name or username
            approved_by = request.user.get_full_name().strip() or request.user.username

            # ✅ Debugging: Print the admin's name
            print(f"DEBUG: Approved By = {approved_by}")

            # ✅ Generate the PDF with admin's name
            pdf_filename = generate_request_pdf(req.id, approved_by)
            req.pdf_file = f"request_pdfs/{pdf_filename}"  # Store relative path
            req.save()  # ✅ Save again after updating the PDF file

            return redirect("admin_requests")

        elif action == "return":
            comments = request.POST.get("comments", "")
            req.comments = comments
            req.status = "returned"
            req.save()
            return redirect("admin_requests")

    return render(request, "approval_system/review_request.html", {"req": req, "form_data": form_data})



