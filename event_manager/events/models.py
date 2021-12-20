from typing import Optional

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from event_manager.users.models import User


class Event(models.Model):
    """
    Events model - Store Events related information
    """

    SING_UP = "sign-up"
    WITHDRAW = "withdraw"
    ACTION = {
        SING_UP: "add",
        WITHDRAW: "remove",
    }
    title = models.CharField(verbose_name=_("Title"), max_length=50)
    description = models.TextField(verbose_name=_("Description"))
    date = models.DateField(verbose_name=_("Date"))
    participants = models.ManyToManyField(to=User, through="Participation")
    owner = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name="owned_events"
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @cached_property
    def display_owner(self):
        user, _ = self.owner.email.split("@")
        return user

    @property
    def number_of_participants(self):
        return self.participants.count()

    def registrate(self, participant: User, action: Optional[str] = None) -> None:
        """
        Method used to add/remove users (participants) for each event
        """
        method = self.ACTION.get(action)
        getattr(self.participants, method)(participant) if method else None


class Participation(models.Model):
    """
    Participation model - Store Relations between Users & Events
    """

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="events_attendance"
    )
    event = models.ForeignKey(
        to=Event, on_delete=models.CASCADE, related_name="participating_users"
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Participation")
        verbose_name_plural = _("Participations")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event} - {self.user}"
