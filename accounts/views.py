from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django_ratelimit.decorators import ratelimit
from .forms import RegisterForm, SecureLoginForm 
from auditlog.models import AuditLog

# --- Helper Function ---
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name="Admin").exists())

# --- Register View (Unchanged) ---
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

# --- UPDATED LOGIN VIEW (With Debugging) ---
@ratelimit(key='ip', rate='5/15m', block=False)
def login_view(request):
    
    # --- DEBUGGING: Watch your terminal! ---
    # This will print "True" if the user has hit the limit
    is_limited = getattr(request, 'limited', False)
    print(f"DEBUG: IP {request.META.get('REMOTE_ADDR')} - Rate Limit Exceeded? {is_limited}")
    # ---------------------------------------

    # 1. SECURITY CHECK: Is this IP already blocked?
    if is_limited:
        print("DEBUG: BLOCKING USER NOW - RENDER 429 PAGE") # Confirm block in terminal
        
        # Log the security event
        AuditLog.objects.create(
            user=None,
            action="SECURITY ALERT: Brute-Force Block Triggered (Rate Limit Exceeded)",
            ip_address=request.META.get("REMOTE_ADDR")
        )
        # Render the custom "Blocked" page with 429 status code
        return render(request, '429.html', status=429)

    # 2. Normal Login Process
    if request.method == "POST":
        form = SecureLoginForm(data=request.POST)
        if form.is_valid():
            # Success: User passed CAPTCHA and Password
            user = form.get_user()
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action="User logged in successfully",
                ip_address=request.META.get("REMOTE_ADDR")
            )
            return redirect("profile")
        else:
            # Failure: Wrong Password or CAPTCHA
            AuditLog.objects.create(
                user=None,
                action=f"Failed login attempt for username: {request.POST.get('username')}",
                ip_address=request.META.get("REMOTE_ADDR")
            )
    else:
        form = SecureLoginForm()
    
    return render(request, "registration/login.html", {"form": form})

# --- Other Views (Unchanged) ---
def home(request):
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

# --- Error Handlers ---
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)