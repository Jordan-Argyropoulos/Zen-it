import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']  # À restreindre en production

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'tickets',
    'chatbot',
]

# Configuration Azure SQL Database
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('AZURE_SQL_NAME'),
        'USER': os.getenv('AZURE_SQL_USER'),
        'PASSWORD': os.getenv('AZURE_SQL_PASSWORD'),
        'HOST': os.getenv('AZURE_SQL_HOST'),
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# JWT Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Azure Blob Storage pour les pièces jointes
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_KEY')
AZURE_CONTAINER = 'tickets-attachments'

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
