from django.conf import settings


def get_client_ip(request):
    """
    リクエストから実クライアント IP を取得する。

    TRUSTED_PROXY_COUNT=0（デフォルト）: REMOTE_ADDR をそのまま返す。
    TRUSTED_PROXY_COUNT=N: X-Forwarded-For を解析し右から N 番目を返す。
      - Railway 本番: TRUSTED_PROXY_COUNT=1 を設定する。

    前提条件:
      全リクエストが信頼プロキシを必ず経由するネットワーク構成
      （例: Railway がアプリへの直接アクセスを遮断）を前提とする。
      直接アクセスが可能な構成では REMOTE_ADDR / XFF を攻撃者が
      制御できるため、レート制限の信頼性はインフラ側の保証に依存する。

    fail-safe:
      XFF のエントリ数が TRUSTED_PROXY_COUNT 未満の場合は
      REMOTE_ADDR にフォールバックする（設定ミスや直接アクセスの疑い）。
      最左要素（最も信頼できない）を採用する fail-open にはしない。
    """
    trusted = getattr(settings, "TRUSTED_PROXY_COUNT", 0)

    if trusted <= 0:
        return request.META.get("REMOTE_ADDR", "")

    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not xff:
        return request.META.get("REMOTE_ADDR", "")

    ips = [ip.strip() for ip in xff.split(",") if ip.strip()]
    if len(ips) < trusted:
        # XFF エントリ数がプロキシ数未満 → 設定ミスまたは直接アクセスの疑い
        # fail-open を避けるため REMOTE_ADDR にフォールバック
        return request.META.get("REMOTE_ADDR", "")

    idx = len(ips) - trusted
    return ips[idx]
