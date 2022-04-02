from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('projects.urls')),
    path('', include('backers.urls')),
    path('', include('emails.urls')),
    path('', include('settings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
