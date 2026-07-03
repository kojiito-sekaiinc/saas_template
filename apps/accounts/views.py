import logging

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.common.utils import get_client_ip

from .forms import LoginForm, SignupForm

logger = logging.getLogger(__name__)

SIGNUP_RATE_LIMIT = 10  # max attempts per hour
SIGNUP_RATE_WINDOW = 3600  # seconds

PASSWORD_RESET_RATE_LIMIT = 5  # max requests per hour
PASSWORD_RESET_RATE_WINDOW = 3600  # seconds


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
        # IP-based rate limiting
        ip = get_client_ip(request)
        cache_key = f"signup_rate_{ip}"
        attempts = cache.get(cache_key, 0)
        if attempts >= SIGNUP_RATE_LIMIT:
            return HttpResponse("Too many signup attempts. Please try again later.", status=429)
        cache.set(cache_key, attempts + 1, SIGNUP_RATE_WINDOW)

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
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
        form = LoginForm(request, request.POST)
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


class RateLimitedPasswordResetView(auth_views.PasswordResetView):
    """IP 単位のレートリミット付きパスワードリセット申請ビュー。

    制限超過時は 429 を返さず、メールを送らずに通常の done 画面へ
    リダイレクトする。挙動を通常時と揃えることで、レート制限の存在や
    メールアドレスの登録有無を外部から観測しにくくする（列挙防止）。
    """

    def post(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        cache_key = f"password_reset_rate_{ip}"
        attempts = cache.get(cache_key, 0)
        if attempts >= PASSWORD_RESET_RATE_LIMIT:
            logger.warning(f"Password reset rate limit exceeded: ip={ip}")
            return redirect(self.get_success_url())
        cache.set(cache_key, attempts + 1, PASSWORD_RESET_RATE_WINDOW)
        return super().post(request, *args, **kwargs)
