import pytest
from django.test import RequestFactory
from django.urls import reverse

from event_manager.events.models import Event
from event_manager.events.views import EventParticipateView
from event_manager.users.models import User

pytestmark = pytest.mark.django_db


class TestEventParticipateView:
    def test_sign_up_participation(self, event: Event, user: User, rf: RequestFactory):
        kwargs = {"pk": event.pk, "action": event.SING_UP}
        # Create an instance of a GET request.
        request = rf.get(reverse("events:participate", kwargs=kwargs))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = user

        assert event.number_of_participants == 0

        # Test EventParticipateView response
        response = EventParticipateView.as_view()(request, **kwargs)
        assert response.status_code == 302
        assert response.url == reverse("events:list")
        assert event.number_of_participants == 1

    def test_get_redirect_url(self, event: Event, user: User, rf: RequestFactory):
        view = EventParticipateView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == "/events/"
