from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import admin_dashboard

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    # outras URLs
    path('', include('core.urls')),  # Inclui as URLs do aplicativo core


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
