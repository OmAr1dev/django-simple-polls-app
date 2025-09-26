from django.contrib import admin

from .models import Choice, Poll, Vote


class ChoiceInline(admin.TabularInline):
    """Custom admin configuration for the Poll model."""

    model = Choice
    extra = 2  # number of extra choices to show


class PollAdmin(admin.ModelAdmin):
    """Custom admin configuration for the Poll model."""

    inlines = [ChoiceInline]
    list_display = ("title", "created_at")


admin.site.register(Poll, PollAdmin)
admin.site.register(Vote)
