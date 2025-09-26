from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm
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
