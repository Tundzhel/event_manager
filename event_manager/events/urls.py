from django.urls import path

from event_manager.events.views import (
    EventCreateView,
    EventListView,
    EventParticipateView,
    EventUpdateView,
)

urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("create/", EventCreateView.as_view(), name="create"),
    path("update/<int:pk>/", EventUpdateView.as_view(), name="update"),
    path(
        "participate/<int:pk>/<slug:action>/",
        EventParticipateView.as_view(),
        name="participate",
    ),
]
