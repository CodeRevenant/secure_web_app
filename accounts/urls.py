# accounts/urls.py
from django.urls import path
from . import views # Imports your custom views with Rate Limiting and Audit Logs

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    
    # ✅ CORRECT: Now using your custom function from views.py
    path("login/", views.login_view, name="login"), 
    
    # ✅ CORRECT: Now using your custom function to record Audit Logs
    path("logout/", views.logout_view, name="logout"),
    
    path("profile/", views.profile, name="profile"),
    path("audit-logs/", views.audit_logs, name="audit_logs"),
]