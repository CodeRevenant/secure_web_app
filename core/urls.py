from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    
    # Required for CAPTCHA images to render [Requirement 2]
    path('captcha/', include('captcha.urls')),
]

# Custom Error Handlers to prevent Information Leakage [Requirement 4]
# These point to views that you will create next
handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'