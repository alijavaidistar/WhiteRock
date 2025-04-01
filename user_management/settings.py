"""
Django settings for user_management project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yher2$uis(8t(3+7=xf2(4=h#@5vke!v%csl2je=#sbq2bboai'

#tailwind configuration
TAILWIND_APP_THEME = 'theme'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "whiterock-b8h3ghfhg9fpd7hw.centralus-01.azurewebsites.net",
    "127.0.0.1",  # Localhost for testing
    'localhost',
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'django.contrib.sites', # microsoft login start
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft', # microsoft login end
    'social_django',
    'approval_system',
    'tailwind',
    'theme'
]

########################
# for microsoft login start
SITE_ID = 2

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.azuread.AzureADOAuth2',  # For Microsoft login
    
)

''' old -- micro login
SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'APP': {
            'client_id': '9f5f96ca-cef4-46a8-8ab7-cc43b050950f',  # Your Client ID
            'secret': '5f10fc5f-22bc-449b-b682-f7541cd85f63',  # Your Secret Key
            'key': '',
        },
        'AUTH_PARAMS': {
            'response_type': 'code',
            'scope': 'openid email profile',
            'tenant': '170bbabd-a2f0-4c90-ad4b-0e8f0f0c4259'  # 🔹 Add your Tenant ID here
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

'''

######## new -- micro login start
SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'tenant': 'organizations',
        'SCOPE': ['openid', 'profile', 'email', 'User.Read'],
        'AUTH_PARAMS': {'response_type': 'code'},
    },
}


######## new -- micro login end




LOGIN_REDIRECT_URL = '/accounts/role_redirect/'
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout





###### redirect to basicrole after sign up with microsoft:
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',  # This creates a new user
    'accounts.pipeline.assign_basic_role',  # Custom function to assign role
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)



# for microsoft login end
########################


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'user_management.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Social Auth Context
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'user_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.User'

