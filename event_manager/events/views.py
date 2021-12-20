from typing import Any, Optional

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from django.db.models import BooleanField, Case, Value, When
from django.http.response import HttpResponseBase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, RedirectView, UpdateView

from event_manager.events.forms import EventForm
from event_manager.events.models import Event


class EventCrudMixin:
    """
    Common functions used in Event CRUD Views
    """

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "owner": self.request.user,
            }
        )
        return kwargs

    def get_success_url(self):
        return reverse("events:list")


class EventListView(LoginRequiredMixin, ListView):
    template_name = "events/list.html"
    model = Event
    paginate_by = 5

    def get_queryset(self) -> models.query.QuerySet:
        """
        Users can see all events and sign up or withdraw but they should only be able to edit their events
        """
        queryset = self.model.objects.annotate(
            can_edit=Case(
                When(owner__pk=self.request.user.pk, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).all()
        return queryset


class EventCreateView(
    LoginRequiredMixin, SuccessMessageMixin, EventCrudMixin, CreateView
):
    model = Event
    form_class = EventForm
    template_name = "events/create.html"
    success_message = _("Event successfully created")


class EventUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, EventCrudMixin, UpdateView
):
    model = Event
    form_class = EventForm
    template_name = "events/update.html"
    success_message = _("Event successfully updated")
    owner = None

    def get_queryset(self) -> models.query.QuerySet:
        """
        Filters all the events that belong to the requester
        """
        return self.model.objects.filter(owner=self.request.user)


class EventParticipateView(LoginRequiredMixin, SuccessMessageMixin, RedirectView):
    pattern_name = "events:list"
    success_message = _("You've successfully participated")

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        """
        Users call this method with desired action (SING_UP = "sign-up" or WITHDRAW = "withdraw")
        In order to join to events
        """
        pk = self.kwargs.get("pk")
        action = self.kwargs.get("action")
        if Event.objects.filter(id=pk).exists():
            event = Event.objects.get(id=pk)
            event.registrate(request.user, action)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(self.pattern_name)
