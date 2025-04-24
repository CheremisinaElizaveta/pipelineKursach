from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as auth_logout
from users.decorators import anonymous_required
from users.forms import RegistrationForm, CustomAuthenticationForm
from users.models import UserGroup
import os

@anonymous_required()
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.user
            django_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/auth.html', {'form': form})

@anonymous_required()
def register(request):
    groups = UserGroup.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'groups': groups})

@login_required(login_url='/users/login/')
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='/users/login/')
def my_recommendations(request):
    return render(request, 'users/my_recommendations.html')

def view_logs(request):
    log_file = os.path.join('logs', 'django_2025-04-24.log')
    
    try:
        with open(log_file, 'r') as f:
            log_lines = f.readlines()[-10:]  # Получаем последние 10 строк
        log_content = ''.join(log_lines)
    except FileNotFoundError:
        log_content = "No log file found."
    
    return render(request, 'users\logs.html', {'log_content': log_content})
