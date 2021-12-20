import pytest

from event_manager.events.models import Event
from event_manager.users.models import User

pytestmark = pytest.mark.django_db


def test_event_successful_registration_and_withdrawal(event: Event, user: User):
    assert event.number_of_participants == 0
    event.registrate(user, event.SING_UP)
    assert event.number_of_participants == 1
    event.registrate(user, event.WITHDRAW)
    assert event.number_of_participants == 0


def test_event_wrong_registration_and_withdrawal(event: Event, user: User):
    assert event.number_of_participants == 0
    event.registrate(user, "some-wrong-action")
    assert event.number_of_participants == 0
    event.registrate(user, "some-wrong-action")
    assert event.number_of_participants == 0


def test_event_display_owner(event: Event):
    assert event.display_owner in event.owner.email
