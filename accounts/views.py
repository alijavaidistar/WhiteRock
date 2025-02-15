from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth import logout  # Correct import
from django.contrib.auth.decorators import login_required



def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signing up
            return redirect(f'/{user.role}/')  # Redirect based on role
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(f'/{user.role}/')  # Redirect to role-based page
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
def staff_home(request):
    return render(request, 'accounts/staff_home.html')

@login_required
def admin_home(request):
    return render(request, 'accounts/admin_home.html')