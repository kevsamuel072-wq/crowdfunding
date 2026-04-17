from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('campaigns.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalización del admin
admin.site.site_header = "FundIt - Panel de Administración"
admin.site.site_title = "FundIt Admin"
admin.site.index_title = "Gestión de la Plataforma"
