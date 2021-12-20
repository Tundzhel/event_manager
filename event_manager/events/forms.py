from django.forms import ModelForm

from event_manager.events.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]

    def __init__(self, owner, **kwargs):
        super(EventForm, self).__init__(**kwargs)
        self.owner = owner

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.owner = self.owner
        super(EventForm, self).save(*args, **kwargs)
