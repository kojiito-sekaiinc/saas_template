from django.conf import settings


def get_client_ip(request):
    """
    リクエストから実クライアント IP を取得する。

    TRUSTED_PROXY_COUNT=0（デフォルト）: REMOTE_ADDR をそのまま返す。
    TRUSTED_PROXY_COUNT=N: X-Forwarded-For の右端 N 番目を返す。
      - Railway 本番: TRUSTED_PROXY_COUNT=1 を設定する。

    XFF 偽装対策:
      クライアントが XFF に任意の IP を付加しても、信頼プロキシが
      末尾に正規 IP を追加するため、右から N 番目を取得することで
      偽装を無効化できる。
    """
    trusted = getattr(settings, "TRUSTED_PROXY_COUNT", 0)

    if trusted <= 0:
        return request.META.get("REMOTE_ADDR", "")

    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not xff:
        return request.META.get("REMOTE_ADDR", "")

    ips = [ip.strip() for ip in xff.split(",")]
    idx = max(0, len(ips) - trusted)
    return ips[idx]
