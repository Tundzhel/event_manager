import pytest

from event_manager.events.forms import EventForm
from event_manager.events.models import Event

pytestmark = pytest.mark.django_db


class TestEventForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_event_form_validation(self, event: Event):
        """
        Tests EventForm unique validator functions correctly
        """
        valid_form = EventForm(
            data={
                "title": event.title,
                "description": event.description,
                "date": event.date,
            },
            owner=event.owner,
        )
        assert valid_form.is_valid()

        invalid_form = EventForm(
            data={
                "description": event.description,
                "date": event.date,
            },
            owner=event.owner,
        )

        assert not invalid_form.is_valid()
        assert len(invalid_form.errors) == 1
        assert "title" in invalid_form.errors
        assert invalid_form.errors["title"][0] == "This field is required."
