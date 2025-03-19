from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Request
from .forms import RequestForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
import os
from django.conf import settings
import json

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

            # Convert form fields to JSON for storage
            new_request.data = form.cleaned_data.get('data', '{}')  # ✅ Default to empty JSON object
            print("Storing Data:", new_request.data)  # ✅ Debug before saving



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

    # Ensure only approved requests can be downloaded
    if req.status != 'approved' or not req.pdf_file:
        return redirect('request_list')

    pdf_path = os.path.join(settings.MEDIA_ROOT, req.pdf_file)
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')


@login_required
@user_passes_test(is_admin)
def review_request(request, request_id):
    req = Request.objects.get(id=request_id)

    # ✅ Debugging: Print `req.data` before processing
    print("Raw Request Data:", req.data)  

    try:
        form_data = json.loads(req.data) if req.data else {}
    except json.JSONDecodeError:
        form_data = {}  # Default to empty dictionary if parsing fails

    print("Parsed Form Data:", form_data)  # ✅ Debug parsed data

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            req.status = "approved"
          # ✅ Generate signed PDF
            pdf_filename = generate_request_pdf(req.id)  # ← No admin_signature argument
            req.pdf_file = f"request_pdfs/{pdf_filename}"  # Store relative path
            req.save()
            return redirect("admin_requests")

        elif action == "return":
            comments = request.POST.get("comments", "")
            req.comments = comments
            req.status = "returned"
            req.save()
            return redirect("admin_requests")

    return render(request, "approval_system/review_request.html", {"req": req, "form_data": form_data})