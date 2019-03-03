# encoding:utf-8
"""
Django settings for MxOnline project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h#kd460u43k1w5_^-_okiwnalsp)33j0_d9(1gl+iut5g6o8m+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
AUTHTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',   
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app1
    'users',
    # app2
    'courses',
    # app3
    'operation',
    # app4
    'organization',
    # 后台管理
    'xadmin',
    'crispy_forms',
    # django验证码
    'captcha',
    # 分页
    'pure_pagination',
    # 富文本编辑器
    'DjangoUeditor',

]

AUTH_USER_MODEL = "users.UserProfile"

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MxOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 配置media
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'MxOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # 引擎
        'NAME': 'xxxxxx',                     # 数据库名称
        'USER': 'root',                         # 数据库用户名
        'PASSWORD': 'xxxxxx',                 # 密码
        'HOST': '127.0.0.1',                    # 主机
        'PORT': 3306,                           # 端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 时区设置


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
# 关联根目录和static文件夹
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 配置email发送服务
EMAIL_HOST = 'smtp.189.cn'              # 邮件服务器
EMAIL_PORT = 25                         # 邮件服务器端口号
EMAIL_HOST_USER = 'xxxxxxxxxx'  	# 邮件用户
EMAIL_HOST_PASSWORD = 'xxxxxx'       	# 邮件用户密码
EMAIL_USE_TLS = False                   # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性)
EMAIL_FROM = 'xxxxxxxxxx'       	# 邮件发件方


# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 分页
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}