from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, SignupForm


def _get_safe_next_url(request, default):
    """Get next URL from request, validating it's safe to redirect to."""
    next_url = request.POST.get("next") or request.GET.get("next") or default
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    return default


def signup_view(request):
    """Handle user registration with ?next= support."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    next_url = _get_safe_next_url(request, settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form, "next": next_url})


def login_view(request):
    """Handle user login with ?next= support."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    next_url = _get_safe_next_url(request, settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form, "next": next_url})


@require_POST
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("home")
