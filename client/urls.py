from django.urls import path

from client.views import CreateBusinessCommentView, CreateEventCommentView, GetUserProfileView, ModifyClientProfileView


urlpatterns = [
    path('modify/', ModifyClientProfileView.as_view(), name='modify-client-profile'),
    path('get-preferences/', GetUserProfileView.as_view(), name='get-client-preferences'),
    path('event/add-comment/', CreateEventCommentView.as_view(), name='add-event-comment'),
    path('business/add-comment/', CreateBusinessCommentView.as_view(), name='add-business-comment'),
]