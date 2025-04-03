from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts.views import basic_home, staff_home, admin_home

from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')  # Use 'accounts/home.html' since it's inside accounts/templates/accounts



urlpatterns = [
  #path('admin/', admin.site.urls),
    path('', home, name='home'),  # Root URL
   path('accounts/', include('accounts.urls')),  # Accounts app URLs

    # if you look in view.py you will see these functions being defined there
    path('basic/', basic_home, name='basic_home'),  # Add basic user route
    path('staff/', staff_home, name='staff_home'),  # Add staff user route
    path('admin/', admin_home, name='admin_home'),  # Add admin user route

        # NEW: Include Approval System URLs
    path('approval/', include('approval_system.urls')), 
]



