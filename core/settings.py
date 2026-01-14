import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file from the root directory
load_dotenv(BASE_DIR / '.env')

# --- SECURE CONFIGURATION (Requirement 7 & 11) ---
# Secrets are pulled from .env to prevent exposure in version control
SECRET_KEY = os.getenv('SECRET_KEY')

# DEBUG should be True for development/marking, False for production testing
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Explicitly allowed hosts for security
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'tasks',
    'auditlog',
    'captcha', # Requirement 2: Bot protection
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Requirement 7 protection
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Essential for custom 404/500 pages
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Requirement 3: Password Complexity Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- SECURITY & SESSION MANAGEMENT (Requirement 2, 7 & 11) ---

# Prevent JavaScript access to cookies to mitigate XSS impact
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Browser-level security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY' # Clickjacking protection

# Requirement 2: 15-minute Session Timeout
SESSION_COOKIE_AGE = 900 
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if not DEBUG:
    # Production security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # NOTE: SECURE_SSL_REDIRECT is disabled to allow local evaluation without HTTPS
else:
    # Development defaults
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Authentication Routes
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/login/'