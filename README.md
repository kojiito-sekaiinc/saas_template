# Django SaaS Subscription Template

A production-ready Django template for building subscription-based SaaS in days, not weeks.  
Includes email-based authentication, 7-day free trial, Stripe subscriptions, secure webhooks, and Customer Portal.  
Designed for fast iteration, safe monetization, and service-by-service SaaS launch.

## Technology Stack

- **Backend**: Django
- **Frontend**: Django Templates + Tailwind CSS
- **Database**: PostgreSQL (SQLite for local development)
- **Payments**: Stripe (subscription model)
- **Deployment**: Railway
- **Static Files**: WhiteNoise

## Runtime

- Python 3.11.x (recommended)
- Python 3.12.x (supported)
- Python 3.14 is NOT supported (Django compatibility issue)

## Local Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables:

```bash
cp .env.example .env
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Collect static files:

```bash
python manage.py collectstatic --noinput
```

This is required before running tests or the dev server. WhiteNoise serves static files in all environments and expects `staticfiles/` to exist.

6. Start the development server:

```bash
python manage.py runserver
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes (production) |
| `DEBUG` | Debug mode (True/False) | No (default: False) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No |
| `SITE_URL` | Base URL of the site. Used to build Stripe Checkout and Portal redirect URLs. If unset in production, Stripe redirects will point to localhost | Yes (production) |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins for CSRF. Auto-populated from `SITE_URL` if HTTPS | No (auto-populated) |
| `DATABASE_URL` | PostgreSQL connection URL | No (uses SQLite if empty) |
| `STRIPE_SECRET_KEY` | Stripe secret API key | Yes (for billing) |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | Yes (for billing) |
| `STRIPE_PRICE_ID` | Stripe Price ID for subscription | Yes (for billing) |
| `TRUSTED_PROXY_COUNT` | Number of trusted reverse proxies (set `1` on Railway) | No (default: `0`) |
| `DJANGO_STATICFILES_MANIFEST` | Enable WhiteNoise `CompressedManifestStaticFilesStorage` for hashed static file URLs. Set `1` in production to enable cache-busting. Requires `collectstatic` to be run first. | No (default: `0`) |

## Project Structure

```
├── apps/
│   ├── accounts/     # Authentication and user profiles
│   ├── billing/      # Stripe integration and subscriptions
│   ├── app/          # Service-specific functionality
│   └── common/       # Shared utilities and middleware
├── config/           # Django project settings
├── templates/        # HTML templates
├── static/           # Static files (CSS, JS, images)
└── requirements.txt  # Python dependencies
```

## Notes

- This is a **reusable template**. When creating new services, modify only `apps/app`.
- Do not change billing or paywall logic unless absolutely necessary.
- Subscription: 980 JPY/month with 7-day free trial (managed by application, not Stripe).

## Known Limitations

### Tailwind CSS (Sekai UI 系) — 本番デプロイ前に必須対応

`ui/layouts/base.html` は開発利便性のため Tailwind Play CDN を使用しています。
本番環境ではこの CDN を **必ず静的ファイルに置き換えてください**。

対応手順：

1. `tailwindcss` CLI で CSS をビルドし `static/css/sekai.css` として配置する
2. `ui/layouts/base.html` の `<script src="https://cdn.tailwindcss.com">` を
   `<link rel="stylesheet" href="{% static 'css/sekai.css' %}">` に置き換える

CDN のまま本番稼働させると、CSP 設定・外部通信制限・オフライン環境において
Sekai UI を使用するすべてのページのスタイルが消失します。

Google Fonts（Inter）も同様に外部 CDN を経由しているため、制限環境では
フォントファイルをセルフホストする対応も併せて実施してください。

### フロントエンド構成（混在期）

現在、以下の 2 系統が混在しています：

- **旧系統**（accounts・billing・home・dashboard）:
  `templates/base.html` → `static/css/app.css`（WhiteNoise 配信）
- **Sekai UI 系**（customers 以降）:
  `ui/layouts/base.html` → Google Fonts CDN + Tailwind CDN（開発用）

新規ページは Sekai UI 系で実装してください。旧系統は将来の移行対象です。
本番前に上記の CDN 対応を Sekai UI 系に対して実施する必要があります。

### ログイン防御の範囲（credential stuffing）

ログイン保護は `django-axes` によるアカウント（email）単位のロックアウトが有効です（5 回失敗で 1 時間ロック）。特定アカウントへの総当たり攻撃は防ぎます。

一方、IP を変えながら多数のアカウントを試す **credential stuffing** はカバー範囲外です。`django-axes` は IP 軸とアカウント軸で個別に閾値を設定できないため、IP ベースの制限を追加すると共有 IP 環境での正当ユーザー誤ロックアウトが発生しやすくなります。この制限は設計上の意図的なトレードオフです。

credential stuffing への対策が必要な場合は、CDN/WAF（Cloudflare 等）やリバースプロキシ側でのレートリミットで補完してください。詳細は `docs/RUNBOOK.md` の「セキュリティ関連の補足」を参照してください。

### Rate Limiting Cache (LocMemCache)

The signup rate limiter uses Django's `LocMemCache`, which is **process-local**.
This works correctly only under the following conditions:

- Single Gunicorn worker (`--workers 1`)
- Single Railway instance (no horizontal scaling)

**Migrate to Redis when any of the following apply:**

- Increasing Gunicorn workers to 2 or more
- Scaling to multiple Railway instances
- Rate limit counters must be shared reliably across processes

Migration steps:
1. Add a Redis plugin on Railway and obtain `REDIS_URL`
2. Add `django-redis` to `requirements.txt`
3. Update `CACHES` in `config/settings.py` to use `django_redis.cache.RedisCache` with `REDIS_URL`
