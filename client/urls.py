from django.urls import path

from client.views import GetUserProfileView, ModifyClientProfileView


urlpatterns = [
    path('modify/', ModifyClientProfileView.as_view(), name='modify-client-profile'),
    path('get-preferences/', GetUserProfileView.as_view(), name='get-client-preferences'),
]