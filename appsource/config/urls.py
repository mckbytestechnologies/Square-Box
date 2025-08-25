"""
URL configuration for velloreland project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib.auth import views as auth_views
from config import app_seo as seo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('mck_auth.urls', namespace='mck_auth')),
    path('mck-master/', include('mck_master.urls', namespace='mck_master')),

    path('change-password/',auth_views.PasswordChangeView.as_view(
                                        extra_context={'page_kwargs':seo.get_page_tags("password_change")}),
                                        name='password_change'),
    path('change-password/complete/',auth_views.PasswordChangeDoneView.as_view(
                                        extra_context={'page_kwargs':seo.get_page_tags("password_change_done")}),
                                        name='password_change_done'),

    path('', include('mck_website.urls', namespace='vlr_website')),
    path('mck-admin-console/', include('mck_admin_console.urls', namespace='mck_admin_console')),
    path('squarebox/', include('squarebox.urls', namespace='squarebox')),

    re_path(r'^app-static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_STATIC_ROOT}),
    re_path(r'^site-media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
