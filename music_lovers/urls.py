from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ml_auth.urls')),
    path('business/', include('business.urls')),
]
