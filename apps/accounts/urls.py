from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"

# パスワードリセットは Django 標準ビューを使用する。
# app_name によるネームスペースがあるため、success_url と
# email テンプレートは明示的に指定する（デフォルトの逆引き名は
# ネームスペースなしの 'password_reset_done' 等を参照するため）。
urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password-reset/",
        # IP 単位のレートリミット付きサブクラス（メール爆撃防止）。
        # 制限超過時も通常の done 画面へ遷移する（列挙防止）。
        views.RateLimitedPasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
            # メール本文の {{ site_name }} はデフォルトではドメイン名になるため、
            # settings.SITE_NAME で上書きする（ブランド名一元化と整合させる）
            extra_email_context={"site_name": settings.SITE_NAME},
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
