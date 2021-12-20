import pytest
from django.urls import resolve, reverse

from event_manager.events.models import Event

pytestmark = pytest.mark.django_db


def test_participate(event: Event):
    assert (
        reverse(
            "events:participate",
            kwargs={
                "pk": event.pk,
                "action": event.SING_UP,
            },
        )
        == f"/events/participate/{event.pk}/{event.SING_UP}/"
    )
    assert (
        resolve(f"/events/participate/{event.pk}/{event.SING_UP}/").view_name
        == "events:participate"
    )


def test_update(event: Event):
    assert (
        reverse(
            "events:update",
            kwargs={
                "pk": event.pk,
            },
        )
        == f"/events/update/{event.pk}/"
    )
    assert resolve(f"/events/update/{event.pk}/").view_name == "events:update"


def test_list():
    assert reverse("events:list") == "/events/"
    assert resolve("/events/").view_name == "events:list"
