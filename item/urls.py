from django.urls import path
from .views import ItemDetailView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'item'

urlpatterns = [
    path("new/", views.new_item, name='new'),
    path('<int:pk>/', ItemDetailView.as_view(), name='detail'),  # Detail view URL pattern
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('', views.items, name='items'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
