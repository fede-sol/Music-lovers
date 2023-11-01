from django.urls import path

from client.views import ModifyClientProfileView


urlpatterns = [
    path('modify/', ModifyClientProfileView.as_view(), name='modify-client-profile'),
]