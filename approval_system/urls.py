from django.urls import path
from .views import submit_request, request_list, admin_requests, approve_request, return_request, download_pdf

urlpatterns = [
    path('submit/', submit_request, name='submit_request'),
    path('requests/', request_list, name='request_list'),  # NEW: Student Request Tracking
    path('admin/requests/', admin_requests, name='admin_requests'),  # Admin view
    path('admin/requests/approve/<int:request_id>/', approve_request, name='approve_request'),
    path('admin/requests/return/<int:request_id>/', return_request, name='return_request'),
    path('requests/download/<int:request_id>/', download_pdf, name='download_pdf'),
]
