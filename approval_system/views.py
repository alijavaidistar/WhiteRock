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
            new_request.returned = False 
         

            # ✅ Exclude file uploads from JSON storage
            '''
            json_ready_data = {}
            for key, value in form.cleaned_data.items():
                if not isinstance(value, InMemoryUploadedFile):  # ✅ Ignore file uploads
                    json_ready_data[key] = value

            # ✅ Store only JSON-serializable data
            new_request.data = json.dumps(json_ready_data)
            '''

            # ✅ Exclude file uploads and convert dates to strings
            json_ready_data = {}
            for key, value in form.cleaned_data.items():
                if not isinstance(value, InMemoryUploadedFile):
                    if hasattr(value, 'isoformat'):  # ✅ Convert date/datetime to string
                        json_ready_data[key] = value.isoformat()
                    else:
                        json_ready_data[key] = value

            new_request.data = json.dumps(json_ready_data)



            print("Storing Data:", new_request.data)  # ✅ Debug before saving

            # ✅ Handle file uploads separately
            if 'signature' in request.FILES:
                new_request.signature = request.FILES['signature']  # ✅ Store file in DB

            new_request.save()
            return redirect('request_list')

    else:
        form = RequestForm(initial={'form_name': form_name}, user=request.user)
        print("🚨 FORM ERRORS:", form.errors)
        print("🧾 FORM DATA:", request.POST.dict())

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









########### 04/20/2025
def is_admin_or_staff(user):
    return user.role in ['admin', 'staff']



from accounts.models import User  # ✅ Make sure this import is at the top
from django.utils import timezone  # ✅ Also make sure this is imported


@login_required
@user_passes_test(is_admin_or_staff)
def review_request(request, request_id):
    req = Request.objects.get(id=request_id)

    # Convert JSON `data` into a Python dictionary
    form_data = json.loads(req.data) if req.data else {}

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            req.status = "approved"
            req.save()

            approved_by = request.user.get_full_name().strip() or request.user.username
            print(f"DEBUG: Approved By = {approved_by}")

            pdf_filename = generate_request_pdf(req.id, approved_by)
            req.pdf_file = f"request_pdfs/{pdf_filename}"
            req.save()


            if request.user.role == "admin":
                return redirect("admin_requests")
            else:
                return redirect("staff_requests")

        elif action == "return":
            comments = request.POST.get("comments", "")
            req.comments = comments
            req.status = "returned"
            req.save()

            if request.user.role == "admin":
                return redirect("admin_requests")
            else:
                return redirect("staff_requests")

        elif action == "delegate":
            delegated_to_id = request.POST.get("delegated_to")
            delegated_to = User.objects.get(id=delegated_to_id)

            req.delegated_to = delegated_to
            req.delegated_by = request.user
            req.delegated_at = timezone.now()
            req.save()

            if request.user.role == "admin":
                return redirect("admin_requests")
            else:
                return redirect("staff_requests")

    # Get staff users in the same unit (excluding current assignee if any)
    staff_users = User.objects.filter(role='staff', unit=req.unit).exclude(id=req.delegated_to_id)

    return render(request, "approval_system/review_request.html", {
        "req": req,
        "form_data": form_data,
        "staff_users": staff_users
    })




from accounts.models import Unit
from django.views.decorators.http import require_http_methods

@login_required
@user_passes_test(is_admin_or_staff)
@require_http_methods(["GET", "POST"])
def assign_units(request):
    print("✅ assign_units view is being triggered")  # ✅ Move this here

    if request.method == "POST":
        req_id = request.POST.get("request_id")
        unit_id = request.POST.get("unit_id")

        req = Request.objects.get(id=req_id)
        unit = Unit.objects.get(id=unit_id)
        req.unit = unit
        req.save()
        return redirect("assign_units")

    unassigned_requests = Request.objects.filter(unit__isnull=True)
    units = Unit.objects.all()

    return render(request, "approval_system/assign_units.html", {
        "unassigned_requests": unassigned_requests,
        "units": units
    })






@login_required
def staff_review_list(request):
    if request.user.role != "staff":
        return redirect("request_list")  # basic user fallback

    requests = Request.objects.filter(unit=request.user.unit, status='pending')


    return render(request, "approval_system/staff_requests.html", {
        "requests": requests
    })



@login_required
def staff_requests_view(request):
    if request.user.role != 'staff':
        return redirect('request_list')  # basic users get redirected

    requests = Request.objects.filter(unit=request.user.unit)

    return render(request, "approval_system/staff_requests.html", {
        "requests": requests
    })




from accounts.models import User, Unit
from django.views.decorators.http import require_http_methods

@login_required
@user_passes_test(lambda u: u.role == "admin")
@require_http_methods(["GET", "POST"])
def manage_staff_units(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        unit_id = request.POST.get("unit_id")

        staff_user = User.objects.get(id=user_id)
        unit = Unit.objects.get(id=unit_id)

        staff_user.unit = unit
        staff_user.save()

        return redirect("manage_staff_units")

    staff_users = User.objects.filter(role="staff")
    units = Unit.objects.all()

    return render(request, "accounts/manage_staff.html", {
        "staff_users": staff_users,
        "units": units
    })
