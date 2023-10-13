from django.urls import path
from business.views import CreateEventView, ModifyEventView

urlpatterns = [
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('modify-event/<int:id_event>/', ModifyEventView.as_view(), name='modify-event'),
   
]