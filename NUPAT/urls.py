from django.contrib import admin
from django.urls import path, include

from core.views import admin_dashboard

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    # outras URLs
    path('', include('core.urls')),  # Inclui as URLs do aplicativo core
]
