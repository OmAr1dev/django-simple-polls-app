from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PollCreateForm, RegisterForm
from .models import Choice, Poll, Vote


def poll_list(request):
    """Display all polls with status (active/closed).
    If a poll is closed, show the winning choice."""
    polls = Poll.objects.all()
    return render(request, "polls/poll_list.html", {"polls": polls})


@login_required
def create_poll(request):
    """
    Single-page poll creation form:
    - enter title
    - select number of choices
    - dynamically show that many choice fields
    """
    if request.method == "POST":
        form = PollCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            num_choices = form.cleaned_data["num_choices"]
            poll = Poll.objects.create(title=title, creator=request.user)
            # Save non-empty choices from POST
            for i in range(1, num_choices + 1):
                choice_text = request.POST.get(f"choice_{i}")
                if choice_text:
                    Choice.objects.create(poll=poll, text=choice_text)
            messages.success(request, "Poll created successfully!")
            return redirect("poll_list")
    else:
        form = PollCreateForm()

    return render(request, "polls/create_poll.html", {"form": form})


@login_required
def poll_detail(request, poll_id):
    """
    Display a single poll, handle voting, allow creator to close or delete the poll.
    """
    poll = get_object_or_404(Poll, id=poll_id)
    voted = Vote.objects.filter(poll=poll, user=request.user).exists()

    # Handle actions
    if request.method == "POST":
        if "close_poll" in request.POST and request.user == poll.creator:
            poll.is_closed = True
            poll.save()
            messages.success(request, "Poll closed successfully!")
            return redirect("poll_detail", poll_id=poll.id)

        elif "delete_poll" in request.POST and request.user == poll.creator:
            poll.delete()
            messages.success(request, "Poll deleted successfully!")
            return redirect("poll_list")

        elif "vote" in request.POST and not voted and not poll.is_closed:
            choice_id = request.POST.get("choice")
            choice = poll.choices.get(id=choice_id)
            choice.votes += 1
            choice.save()
            Vote.objects.create(poll=poll, user=request.user, choice=choice)
            messages.success(request, "Your vote has been recorded!")
            return redirect("poll_detail", poll_id=poll.id)

    # Pass both "voted" and "poll.is_closed" to template
    return render(
        request,
        "polls/poll_detail.html",
        {
            "poll": poll,
            "voted": voted,
        },
    )


def register_view(request):
    """
    Handle user registration.
    On POST: create a new user and log them in.
    On GET: display registration form.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("poll_list")
    else:
        form = RegisterForm()
    return render(request, "polls/register.html", {"form": form})


def login_view(request):
    """
    Handle user login.
    On POST: authenticate user credentials.
    On GET or invalid login: display login form with errors if any.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("poll_list")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "polls/login.html")


def logout_view(request):
    """
    Log out the current user and redirect to poll list.
    """
    logout(request)
    return redirect("poll_list")
