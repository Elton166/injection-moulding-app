from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models_auth import Company, UserProfile
from .forms_auth import (
    CompanyRegistrationForm, CompanyLoginForm,
    ManagerSupervisorRegistrationForm, UserLoginForm
)


def company_register(request):
    """Company registration view"""
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.password_hash = make_password(form.cleaned_data['password'])
            company.save()
            
            # Store company ID in session
            request.session['company_id'] = company.id
            request.session['company_name'] = company.name
            request.session['is_company'] = True
            
            messages.success(request, f'Company {company.name} registered successfully!')
            return redirect('company_dashboard')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'moulding/auth/company_register.html', {'form': form})


def company_login(request):
    """Company login view"""
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                company = Company.objects.get(username=username, is_active=True)
                if check_password(password, company.password_hash):
                    # Store company info in session
                    request.session['company_id'] = company.id
                    request.session['company_name'] = company.name
                    request.session['is_company'] = True
                    
                    messages.success(request, f'Welcome back, {company.name}!')
                    return redirect('company_dashboard')
                else:
                    messages.error(request, 'Invalid password!')
            except Company.DoesNotExist:
                messages.error(request, 'Company not found!')
    else:
        form = CompanyLoginForm()
    
    return render(request, 'moulding/auth/company_login.html', {'form': form})


def company_dashboard(request):
    """Company dashboard view"""
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, 'Please login as a company first!')
        return redirect('company_login')
    
    company = Company.objects.get(id=company_id)
    employees = UserProfile.objects.filter(company=company)
    
    context = {
        'company': company,
        'employees': employees,
        'managers': employees.filter(role='manager'),
        'supervisors': employees.filter(role='supervisor'),
        'operators': employees.filter(role='operator'),
    }
    
    return render(request, 'moulding/auth/company_dashboard.html', context)


def manager_supervisor_register(request):
    """Manager/Supervisor registration view (only accessible by company)"""
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, 'Please login as a company first!')
        return redirect('company_login')
    
    company = Company.objects.get(id=company_id)
    
    if request.method == 'POST':
        form = ManagerSupervisorRegistrationForm(request.POST)
        if form.is_valid():
            # Create Django user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                company=company,
                role=form.cleaned_data['role'],
                employee_id=form.cleaned_data['employee_id'],
                phone=form.cleaned_data.get('phone', ''),
                department=form.cleaned_data.get('department', ''),
                created_by=company
            )
            
            messages.success(request, f'{form.cleaned_data["role"].title()} {user.get_full_name()} registered successfully!')
            return redirect('company_dashboard')
    else:
        form = ManagerSupervisorRegistrationForm()
    
    return render(request, 'moulding/auth/manager_supervisor_register.html', {
        'form': form,
        'company': company
    })


def user_login(request):
    """Manager/Supervisor/Operator login view"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Get user profile
                try:
                    profile = UserProfile.objects.get(user=user)
                    request.session['user_role'] = profile.role
                    request.session['company_id'] = profile.company.id
                    request.session['company_name'] = profile.company.name
                    
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('dashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, 'User profile not found!')
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = UserLoginForm()
    
    return render(request, 'moulding/auth/user_login.html', {'form': form})


def logout_view(request):
    """Logout view for both company and users"""
    if request.user.is_authenticated:
        logout(request)
    
    # Clear all session data
    request.session.flush()
    
    messages.success(request, 'Logged out successfully!')
    return redirect('login_home')


def login_home(request):
    """Home page with login options"""
    return render(request, 'moulding/auth/login_home.html')
