from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Sum


class Poll(models.Model):
    """Represents a poll or survey question that users can vote on."""

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_polls"
    )
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        """Return the title of the poll as its string representation."""
        return self.title

    def total_votes(self):
        """Return total votes across all choices."""
        return self.choices.aggregate(total=Sum("votes"))["total"] or 0

    def get_winner(self):
        """
        Returns:
            - None if no votes at all
            - A list of winning choices if there’s a tie
            - A list with one choice if there’s a single winner
        """
        if self.total_votes() == 0:
            return None

        max_votes = self.choices.aggregate(max_votes=Max("votes"))["max_votes"]
        winners = list(self.choices.filter(votes=max_votes))
        return winners


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
