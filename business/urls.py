from django.urls import path
from business.views import AddImageBusinessView, AddImageEventView, BusinessEventsView, CreateEventView, ModifyBusinessView, ModifyEventView, CreateBusinessView, DeleteEventView, FilterEventsView, FilterBusinessView

urlpatterns = [
    path('create/', CreateBusinessView.as_view(), name='create-business'),
    path('add-image/', AddImageBusinessView.as_view(), name='add-image-business'),
    path('modify/', ModifyBusinessView.as_view(), name='modify-business'),
    path('events/', BusinessEventsView.as_view(), name='list-events'),
    path('event/create/', CreateEventView.as_view(), name='create-event'),
    path('event/modify/', ModifyEventView.as_view(), name='modify-event'),
    path('event/add-image/', AddImageEventView.as_view(), name='add-image-event'),
    path('event/delete-event/', DeleteEventView.as_view(), name='delete-event'),
    path('events/get/', FilterEventsView.as_view(), name='filter-events'),
    path('get/', FilterBusinessView.as_view(), name='filter-business')
]