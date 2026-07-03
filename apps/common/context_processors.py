"""
共通 context processor。

全テンプレートにサイト共通の値を渡す。ブランド名は settings.SITE_NAME
（env var SITE_NAME）に一元化し、テンプレート側は {{ site_name }} で参照する。
"""
from django.conf import settings


def site(request):
    return {"site_name": settings.SITE_NAME}
