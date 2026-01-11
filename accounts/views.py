from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, SecureLoginForm 
from auditlog.models import AuditLog

def is_admin(user):
    # Check if user is staff (admin) or in Admin group
    return user.is_authenticated and (user.is_staff or user.groups.filter(name="Admin").exists())

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            AuditLog.objects.create(
                user=user,
                action=f"New user registered: {user.username}",
                ip_address=request.META.get("REMOTE_ADDR")
            )
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = SecureLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action="User logged in successfully",
                ip_address=request.META.get("REMOTE_ADDR")
            )
            return redirect("profile")
        else:
            AuditLog.objects.create(
                user=None,
                action=f"Failed login attempt for username: {request.POST.get('username')}",
                ip_address=request.META.get("REMOTE_ADDR")
            )
    else:
        form = SecureLoginForm()
    return render(request, "registration/login.html", {"form": form})

def home(request):
    """Public homepage for the site."""
    form = SecureLoginForm()
    return render(request, "home.html", {"login_form": form})

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def logout_view(request):
    AuditLog.objects.create(
        user=request.user,
        action="User logged out",
        ip_address=request.META.get("REMOTE_ADDR")
    )
    logout(request)
    return redirect("login")

@user_passes_test(is_admin)
def audit_logs(request):
    logs = AuditLog.objects.all().order_by("-timestamp")
    return render(request, "audit_logs.html", {"logs": logs})

# --- MANDATORY ERROR HANDLERS [Requirement 4] ---

def custom_404(request, exception):
    """Prevents information leakage by hiding technical 404 details"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Prevents information leakage by hiding stack traces on server errors"""
    return render(request, '500.html', status=500)