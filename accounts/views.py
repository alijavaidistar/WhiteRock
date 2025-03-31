
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
    # Check if the request method is POST, indicating the form has been submitted
    if request.method == "POST":

        # Initialize the SignUpForm with the submitted data (request.POST)
        form = SignUpForm(request.POST)

        # If the form is valid (i.e., no required fields are missing and all validations pass)
        if form.is_valid():

            # 'commit=False' prevents saving the user object to the database just yet
            # This allows us to make changes to the object (like setting the role)
            user = form.save(commit=False)
            user.role = "basic"  # Assign a default role ('basic') to the new user
            user.save()  # Save the user object to the database

            # Set the authentication backend manually for the user (Django default backend)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # Log the user in immediately after saving
            login(request, user, backend=user.backend)

            # After successful sign-up and login, redirect the user to the 'basic' page
            return redirect('/basic/')  # Fix redirect path to where basic users should go
    else:
        # If the request method is GET (user is visiting the page for the first time),
        # create an empty sign-up form
        form = SignUpForm()
    
    # Render the sign-up page with the form (either empty or with validation errors)
    return render(request, 'accounts/sign_up.html', {'form': form})
    # 'request': The HTTP request object (provides details about the incoming request)
    # 'accounts/sign_up.html': The template to be rendered
    # {'form': form}: The context data to be passed to the template (in this case, the form object)


# This function handles the user login process
def login_view(request):

    # Check if the request method is POST (i.e., form was submitted)
    if request.method == "POST":

        # Create an instance of the AuthenticationForm, populated with POST data from the request
        form = AuthenticationForm(request, data=request.POST)

        # Check if the form is valid (i.e., required fields are filled in correctly)
        if form.is_valid():

            # Get the cleaned data for the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user using the username and password
            user = authenticate(username=username, password=password)

            # If the user is successfully authenticated
            if user is not None:
                # Explicitly set the backend for authentication (this tells Django to use the default backend)
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # Log the user in by calling the login function
                login(request, user, backend=user.backend)

                # Redirect the user based on their role
                if user.role == "admin":
                    # Redirect to the admin dashboard for admins
                    return redirect('/admin/')
                elif user.role == "staff":
                    # Redirect to the staff dashboard for staff members
                    return redirect('/staff/')
                else:
                    # Redirect to the basic user dashboard for regular users
                    return redirect('/basic/')

    # If the request method is not POST (i.e., initial page load), create an empty form
    else:
        form = AuthenticationForm()

    # Render the 'login.html' template and pass the form to it as context
    return render(request, 'accounts/login.html', {'form': form})
    # 'request': The HTTP request object (provides details about the incoming request)
    # 'accounts/login.html': The template to be rendered
    # {'form': form}: The context data to be passed to the template (in this case, the form object)




# This function handles the logout process
def logout_view(request):
    
    # Call Django's built-in logout function to log the user out
    logout(request)

    # Redirect the user to the login page after logging them out
    return redirect('/accounts/login/')  # Redirect to the login page










# The @login_required decorator ensures that the user is authenticated before accessing this view
@login_required
def basic_home(request):
    # Renders the basic home page for authenticated users
    return render(request, 'accounts/basic_home.html', {'user': request.user})

# The @login_required decorator ensures that the user is authenticated before accessing this view
@login_required
def role_based_redirect(request):
    """ Redirect users to their role-based home page after login """
    
    # Get the current user object
    user = request.user
    
    # Redirect based on the user's role
    if user.role == "admin":
        # Redirect admin users to the admin home page
        return redirect('/accounts/admin_home/')
    elif user.role == "staff":
        # Redirect staff users to the staff home page
        return redirect('/accounts/staff_home/')
    
    # Default redirect for new users or basic role users
    return redirect('/accounts/basic_home/')  # Redirect to the basic home page

# The @login_required decorator ensures that the user is authenticated before accessing this view
@login_required
def staff_home(request):
    """Staff Dashboard - Display basic user and staff statistics"""
    if request.user.role != "staff":  # Ensure only staff can access
        return redirect('/accounts/basic_home/')

    # Fetch user statistics for staff
    total_users = User.objects.filter(role="staff").count() + User.objects.filter(role="basic").count()
    staff_count = User.objects.filter(role="staff").count()
    basic_count = User.objects.filter(role="basic").count()

    return render(request, 'accounts/staff_home.html', {
        'total_users': total_users,
        'staff_count': staff_count,
        'basic_count': basic_count,
    })


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




@login_required
def admin_users_view(request):
    """ Fetch all users and their roles for the admin or staff dashboard """
    
    if request.user.role == "admin":  # Only admins can access this
        users = User.objects.all().order_by('-date_joined')  # Fetch all users for admin view
        return render(request, 'accounts/admin_users.html', {'users': users})
    
    elif request.user.role == "staff":  # If the user is staff
        # Staff can view both basic users and staff users, but not admin users
        users = User.objects.filter(role__in=["basic", "staff"]).order_by('-date_joined')
        return render(request, 'accounts/staff_users.html', {'users': users})
    
    else:
        # Redirect if the user doesn't have admin or staff role
        return redirect('/accounts/basic_home/')




#### admin features to delete decactaive and change roles
@login_required
def change_role(request, user_id):
    """Allow Admin and Staff to change user roles."""
    if request.user.role not in ["admin", "staff"]:
        # Redirect if the user doesn't have permission (neither admin nor staff)
        return redirect('/accounts/basic_home/')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("new_role")
        if new_role in ["basic", "staff", "admin"]:
            user.role = new_role
            user.save()
            messages.success(request, f"Updated role of {user.username} to {new_role}.")
    
    # After role change, redirect to the appropriate users management page based on the user's role
    if request.user.role == "admin":
        return redirect('/accounts/admin/users/')
    elif request.user.role == "staff":
        return redirect('/accounts/staff/users/')

    
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