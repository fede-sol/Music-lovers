from django.urls import path
from ml_auth.views import BusinessLoginView, BusinessSignupView, ClientLoginView, ClientSignupView

urlpatterns = [
    path('business/login/', BusinessLoginView.as_view(),name='login'),
    path('business/register/', BusinessSignupView.as_view(),name='register'),
    path('client/login/', ClientLoginView.as_view(),name='login'),
    path('client/register/', ClientSignupView.as_view(),name='register'),
]
