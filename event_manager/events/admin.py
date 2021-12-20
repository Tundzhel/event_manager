from django.contrib import admin

from event_manager.events.models import Event, Participation


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 2


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "date",
        "get_owner",
        "created_at",
        "updated_at",
    ]
    search_fields = ["title"]
    inlines = [ParticipationInline]

    @admin.display(description="Owner")
    def get_owner(self, obj):
        return obj.owner.email
