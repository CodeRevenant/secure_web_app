from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view
from .forms import SecureLoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(authentication_form=SecureLoginForm), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/login/"),
        name="logout",
    ),
    path("profile/", views.profile, name="profile"),
    path("audit-logs/", views.audit_logs, name="audit_logs"),
]
