from django.urls import path
from business.views import AddImageBusinessView, AddImageEventView, CreateEventView, ModifyEventView, CreateBusinessView

urlpatterns = [
    path('create/', CreateBusinessView.as_view(), name='create-business'),
    path('add-image/', AddImageBusinessView.as_view(), name='add-image-business'),
    path('event/create/', CreateEventView.as_view(), name='create-event'),
    path('event/modify/<int:id_event>/', ModifyEventView.as_view(), name='modify-event'),
    path('event/add-image/', AddImageEventView.as_view(), name='add-image-event'),

]