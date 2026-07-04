import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Muat variabel dari file .env (kalau ada) supaya SECRET_KEY & DEBUG
# tidak perlu di-hardcode di source code.
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

# ========================
# SECURITY
# ========================
# SECRET_KEY WAJIB diisi lewat environment variable saat production.
# Nilai default di bawah HANYA untuk kebutuhan development lokal.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-hlf##8_l9!5wmp1rkny8c9h0)p=184*m-tvmu49zeb3hbo)zr^'
)

# DEBUG harus False di production. Set DJANGO_DEBUG=False di environment
# server produksi. Default True supaya development lokal tetap mudah.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').strip().lower() == 'true'

# Daftar host/domain yang boleh mengakses aplikasi ini.
# Contoh di server: DJANGO_ALLOWED_HOSTS=tokoborneo.com,www.tokoborneo.com
_allowed_hosts_env = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if _allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_env.split(',') if h.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'accounts',
    'kategori',
    'produk',
    'supplier',
    'transaksi',
    'dashboard',
    'laporan',
    'pengaturan',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database — PostgreSQL di production, SQLite untuk development lokal.
# Set DB_ENGINE=postgresql di environment untuk aktifkan PostgreSQL.
_db_engine = os.environ.get('DB_ENGINE', 'sqlite3')

if _db_engine == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'inventory_borneo'),
            'USER': os.environ.get('DB_USER', 'borneo'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.User'

# ========================
# AUTH REDIRECTS
# ========================
LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'id'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Jakarta'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Folder output collectstatic (dipakai di production oleh Nginx/WhiteNoise)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise — compressed & cached static files
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ========================
# PRODUCTION / PROXY
# ========================
# CSRF trusted origins — wajib diisi saat di belakang reverse proxy / Coolify
_csrf_origins = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '')
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]

# Supaya Django tahu request aslinya HTTPS meskipun proxy pakai HTTP
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
