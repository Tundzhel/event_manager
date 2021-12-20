from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from event_manager.events.models import Event
from event_manager.users.tests.factories import UserFactory


class EventFactory(DjangoModelFactory):
    title = Faker("name")
    description = Faker("name")
    date = Faker("date")
    owner = SubFactory(UserFactory)

    class Meta:
        model = Event
