from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('item.urls')),
    path("", include('core.urls')),
    path('inbox', include('conversation.urls')),
    path("", include("django.contrib.auth.urls")),
    path('accounts/', include('allauth.urls')),
]

# Add serving of static files for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
