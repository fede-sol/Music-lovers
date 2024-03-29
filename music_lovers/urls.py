from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ml_auth.urls')),
    path('business/', include('business.urls')),
    path('client/', include('client.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + staticfiles_urlpatterns()
