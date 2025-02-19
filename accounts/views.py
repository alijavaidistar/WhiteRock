
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm
from .models import User  # Import custom User model
from django.contrib import messages


'''
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Explicitly set the backend for authentication
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=user.backend)

            return redirect(f'/{user.role}/')  # Redirect based on role
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/sign_up.html', {'form': form})
'''

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "basic"  # Set default role
            user.save()

            # Explicitly set the backend for authentication
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=user.backend)

            return redirect('/basic/')  # ✅ Fix redirect
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/sign_up.html', {'form': form})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "basic"  # Force the role to "basic"
            user.save()

            # Explicitly set the backend for authentication
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=user.backend)

            return redirect('/accounts/basic_home/')  # Redirect all new users to basic_home
        else:
            print(form.errors)  # Debug: Print validation errors

    else:
        form = SignUpForm()
    
    return render(request, 'accounts/sign_up.html', {'form': form})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "basic"  # Force the role to "basic"
            user.save()

            # Explicitly set the backend for authentication
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=user.backend)

            return redirect('/accounts/basic_home/')  # Redirect all new users to basic_home
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/sign_up.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                # ✅ Explicitly set backend for authentication
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=user.backend)

                # ✅ Redirect based on role
                if user.role == "admin":
                    return redirect('/admin/')  # Redirect admins properly
                elif user.role == "staff":
                    return redirect('/staff/')
                else:
                    return redirect('/basic/')
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                # ✅ Explicitly set backend for authentication
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=user.backend)

                return redirect(f'/{user.role}/')  # Redirect based on role
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')









@login_required
def basic_home(request):
    return render(request, 'accounts/basic_home.html')

@login_required
def role_based_redirect(request):
    """ Redirect users to their role-based home page after login """
    user = request.user
    if user.role == "admin":
        return redirect('/accounts/admin_home/')
    elif user.role == "staff":
        return redirect('/accounts/staff_home/')
    return redirect('/accounts/basic_home/')  # Default for new Microsoft signups




@login_required
def staff_home(request):
    return render(request, 'accounts/staff_home.html')


@login_required
def admin_home(request):
    """Admin Dashboard - Display user statistics"""
    if request.user.role != "admin":  # Ensure only admins can access
        return redirect('/accounts/basic_home/')

    # Fetch user statistics
    total_users = User.objects.count()
    staff_count = User.objects.filter(role="staff").count()
    admin_count = User.objects.filter(role="admin").count()

    return render(request, 'accounts/admin_home.html', {
        'total_users': total_users,
        'staff_count': staff_count,
        'admin_count': admin_count,
    })




# fetches the number of users to display on the admin dashboard
@login_required
def admin_users_view(request):
    """ Fetch all users and their roles for the admin dashboard """
    if request.user.role != "admin":  # Ensure only admins can access
        return redirect('/accounts/basic_home/')  # Redirect non-admins

    users = User.objects.all().order_by('-date_joined')  # Fetch users sorted by date
    return render(request, 'accounts/admin_users.html', {'users': users})




#### admin features to delete decactaive and change roles
@login_required
def change_role(request, user_id):
    """Admin can change user role."""
    if request.user.role != "admin":
        return redirect('/accounts/basic_home/')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("new_role")
        if new_role in ["basic", "staff", "admin"]:
            user.role = new_role
            user.save()
            messages.success(request, f"Updated role of {user.username} to {new_role}.")
    
    return redirect('/accounts/admin/users/')

@login_required
def deactivate_user(request, user_id):
    """Admin can activate/deactivate a user."""
    if request.user.role != "admin":
        return redirect('/accounts/basic_home/')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.is_active = not user.is_active  # Toggle status
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} has been {status}.")

    return redirect('/accounts/admin/users/')

@login_required
def delete_user(request, user_id):
    """Admin can delete a user."""
    if request.user.role != "admin":
        return redirect('/accounts/basic_home/')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, f"Deleted user {user.username}.")

    return redirect('/accounts/admin/users/')

    """Admin can delete a user."""
    if request.user.role != "admin":
        return redirect('/accounts/basic_home/')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, f"Deleted user {user.username}.")

    return redirect('/accounts/admin/users/')