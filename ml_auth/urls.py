from django.urls import path
from ml_auth.views import BusinessLoginView, BusinessSignupView

urlpatterns = [
    path('business/login/', BusinessLoginView.as_view(),name='login'),
    path('business/register/', BusinessSignupView.as_view(),name='register'),
]
