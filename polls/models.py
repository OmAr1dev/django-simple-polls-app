from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    """Represents a poll or survey question that users can vote on."""

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the title of the poll as its string representation."""
        return self.title


class Choice(models.Model):
    """Represents an individual choice option within a poll."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the text of the choice as its string representation."""
        return self.text


class Vote(models.Model):
    """Records an individual vote cast by a user for a specific choice in a poll."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        """Meta configuration for the Vote model."""

        unique_together = ("poll", "user")  # Prevent multiple votes per user
