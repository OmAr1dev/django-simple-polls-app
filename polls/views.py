from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Poll, Vote


def poll_list(request):
    """Display all polls"""
    polls = Poll.objects.all()
    return render(request, "polls/poll_list.html", {"polls": polls})


@login_required
def poll_detail(request, poll_id):
    """Display a single poll and handle voting"""
    poll = get_object_or_404(Poll, id=poll_id)
    voted = Vote.objects.filter(poll=poll, user=request.user).exists()

    if request.method == "POST" and not voted:
        choice_id = request.POST.get("choice")
        choice = poll.choices.get(id=choice_id)
        choice.votes += 1
        choice.save()
        Vote.objects.create(poll=poll, user=request.user, choice=choice)
        messages.success(request, "Your vote has been recorded!")
        return redirect("poll_detail", poll_id=poll.id)

    return render(request, "polls/poll_detail.html", {"poll": poll, "voted": voted})
