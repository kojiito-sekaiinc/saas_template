# Django SaaS Subscription Template

メール認証・7日間無料トライアル・Stripe サブスクリプション・Customer Portal を備えた
本番対応 Django テンプレート。新サービスを数週間ではなく数日でリリースするために設計されています。

---

## What you get

このテンプレートでできること:

- メール認証付きユーザー管理
- Stripe サブスクリプション
- 7日間無料トライアル
- Webhook ベースの課金同期
- 障害時の課金復旧（sync コマンド）
- CI + 本番設定チェック

---

## Quick Start（5分で起動）

```bash
# 1. 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. 依存パッケージをインストール
pip install -r requirements.txt

# 3. 環境変数をコピーして編集
cp .env.example .env
# .env の最低設定例（開発用）:
#
#   SECRET_KEY=your-secret-key
#   SITE_URL=http://localhost:8000
#
#   # Stripe（開発時はダミーでOK）
#   STRIPE_SECRET_KEY=sk_test_dummy
#   STRIPE_PRICE_ID=price_dummy
#   STRIPE_WEBHOOK_SECRET=whsec_dummy

# 4. DB セットアップ
python manage.py migrate

# 5. 静的ファイルを収集（本番時のみ必要）
# python manage.py collectstatic --noinput

# 6. 開発サーバーを起動
python manage.py runserver
```

ブラウザで http://localhost:8000 を開いてください。

---

## Technology Stack

| 分類 | 技術 |
|---|---|
| Backend | Django |
| Frontend | Django Templates + Tailwind CSS |
| Database | PostgreSQL（本番）/ SQLite（ローカル開発） |
| Payments | Stripe（サブスクリプション） |
| Deployment | Railway |
| Static Files | WhiteNoise |

**Runtime:** Python 3.11.x（推奨）/ 3.12.x（サポート）
Python 3.14 は Django 互換性の問題により非対応。

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django シークレットキー | Yes（本番） |
| `DEBUG` | デバッグモード（True/False）| No（デフォルト: False） |
| `ALLOWED_HOSTS` | 許可するホスト名（カンマ区切り）| No |
| `SITE_URL` | サイトの Base URL。Stripe Checkout・Portal のリダイレクト先に使用。未設定だと localhost 向けになる | Yes（本番） |
| `CSRF_TRUSTED_ORIGINS` | CSRF 許可オリジン（カンマ区切り）。HTTPS の SITE_URL から自動補完 | No（自動補完） |
| `DATABASE_URL` | PostgreSQL 接続 URL | No（空なら SQLite） |
| `STRIPE_SECRET_KEY` | Stripe シークレット API キー | Yes（課金機能） |
| `STRIPE_WEBHOOK_SECRET` | Stripe Webhook 署名シークレット | Yes（課金機能） |
| `STRIPE_PRICE_ID` | サブスクリプション用 Stripe Price ID | Yes（課金機能） |
| `TRUSTED_PROXY_COUNT` | 信頼するリバースプロキシ数（Railway 本番: `1`）| No（デフォルト: `0`） |
| `DJANGO_STATICFILES_MANIFEST` | WhiteNoise の manifest モードを有効化。本番で cache-busting を使う場合は `1`。`collectstatic` 実行が前提 | No（デフォルト: `0`） |

---

## Testing

テストランナーは **pytest** に統一されています。`python manage.py test` は使用しないでください。

```bash
# 全テスト実行
pytest

# アプリを絞って実行
pytest apps/billing/
pytest apps/common/

# 特定ファイルを実行
pytest apps/billing/test_sync.py

# 全品質チェック（compile + Django check + pytest）
./scripts/checks/quick_check.sh
```

`django.test.TestCase` ベースのテスト（`apps/accounts/tests.py`）も pytest で自動検出・実行されます。

---

## Pre-deploy Check

本番デプロイ前に設定不備を検出するコマンドが用意されています。

```bash
# テキスト形式で確認
python manage.py check_deploy_config

# JSON 形式（CI やスクリプト連携用）
python manage.py check_deploy_config --json

# WARNING でも失敗扱いにしたい場合
python manage.py check_deploy_config --fail-on-warning
```

**出力例（本番想定）:**

```
OK       DEBUG                    DEBUG=False
OK       SITE_URL                 https://example.com
OK       ALLOWED_HOSTS            example.com
OK       SITE_URL_IN_ALLOWED_HOSTS example.com in ALLOWED_HOSTS
OK       CSRF_TRUSTED_ORIGINS     ok
OK       STRIPE_SECRET_KEY        set
OK       STRIPE_PRICE_ID          price_live_xxx
OK       STRIPE_WEBHOOK_SECRET    set

Summary: ok=8 warning=0 error=0
```

ERROR が 1 件でもあると exit(1) になります。詳細は `docs/RUNBOOK.md` を参照してください。

---

## Deploy

Railway を使用:

1. GitHub リポジトリを接続
2. 環境変数を設定（[Environment Variables](#environment-variables) 参照）
3. Deploy

デプロイ前に必ず実行:

```bash
python manage.py check_deploy_config --fail-on-warning
```

---

## Project Structure

```
├── apps/
│   ├── accounts/     # 認証・ユーザープロフィール（free_until）
│   ├── billing/      # Stripe 連携・サブスクリプション管理
│   ├── app/          # サービス固有の機能（新機能はここだけ追加）
│   └── common/       # Paywall ミドルウェア・共有ユーティリティ
├── config/           # Django 設定
├── templates/        # HTML テンプレート（旧系統）
├── ui/               # Sekai UI コンポーネント・レイアウト
├── static/           # 静的ファイル
└── docs/             # RUNBOOK・仕様書
```

---

## Core Business Rules

- **サブスクリプション**: 月額 980 JPY、単一プランのみ
- **無料トライアル**: 登録後 7 日間（`Profile.free_until` で管理、Stripe の trial 機能は使用しない）
- **有料ゾーン**: `/app/` 配下すべて（`PaywallMiddleware` が保護）
- **アクセス条件**: 無料期間内 OR `BillingProfile.status == "active"`
- **課金状態の正本**: Stripe Webhook（フロントエンドのリダイレクトやクエリパラメータは使用しない）

---

## Known Limitations

### Tailwind CSS（Sekai UI）— 本番デプロイ前に必須対応

`ui/layouts/base.html` は開発利便性のため Tailwind Play CDN を使用しています。
本番環境ではこの CDN を **必ず静的ファイルに置き換えてください**。

対応手順:
1. `tailwindcss` CLI で CSS をビルドし `static/css/sekai.css` として配置する
2. `<script src="https://cdn.tailwindcss.com">` を `<link rel="stylesheet" href="{% static 'css/sekai.css' %}">` に置き換える

CDN のまま本番稼働させると、CSP 設定・外部通信制限・オフライン環境でスタイルが消失します。
Google Fonts（Inter）も同様に外部 CDN を経由しているため、制限環境ではセルフホストしてください。

### フロントエンド構成（混在期）

現在 2 系統が混在しています:

- **旧系統**（accounts・billing・home・dashboard）: `templates/base.html` → `static/css/app.css`
- **Sekai UI 系**（customers 以降）: `ui/layouts/base.html` → Tailwind CDN（開発用）

新規ページは Sekai UI 系で実装してください。旧系統は将来の移行対象です。

### ログイン防御の範囲

`django-axes` によるアカウント（email）単位のロックアウトが有効です（5 回失敗で 1 時間ロック）。
IP を変えながら多数アカウントを試す **credential stuffing** はカバー範囲外です（設計上の意図的なトレードオフ）。
詳細は `docs/RUNBOOK.md` の「セキュリティ」セクションを参照してください。

### Rate Limiting Cache（LocMemCache）

サインアップのレートリミットは `LocMemCache`（プロセスローカル）を使用しています。
以下の条件を満たす場合のみ正常に機能します:

- Gunicorn シングルワーカー（`--workers 1`）
- Railway シングルインスタンス（水平スケールなし）

複数ワーカー・複数インスタンスに移行する際は Redis（`django-redis`）へ切り替えてください。
