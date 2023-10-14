from django.urls import path
from business.views import AddImageBusinessView, CreateEventView, ModifyEventView, CreateBusinessView

urlpatterns = [
    path('create/', CreateBusinessView.as_view(), name='create-business'),
    path('add-image/', AddImageBusinessView.as_view(), name='add-image-business'),
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('modify-event/<int:id_event>/', ModifyEventView.as_view(), name='modify-event'),

]