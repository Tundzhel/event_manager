import pytest

from event_manager.events.models import Event
from event_manager.events.tests.factories import EventFactory
from event_manager.users.models import User
from event_manager.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def event() -> Event:
    return EventFactory()
