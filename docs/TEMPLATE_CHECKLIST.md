# TEMPLATE_CHECKLIST — New SaaS in 2 Weeks (Django + Stripe Subscription Template)

このチェックリストは、このテンプレから新しいSaaSを立ち上げるときに
**考えることを最小化**するための手順です。

---

## 1) 新規プロジェクト作成（最初の30分）
- [ ] GitHubでテンプレから新規リポジトリ作成（Use this template）
- [ ] clone
- [ ] `.env` 作成：`cp .env.example .env`
- [ ] `SECRET_KEY` を新規生成して設定
- [ ] `SITE_URL` をローカルに（`http://localhost:8000`）
- [ ] 依存関係を入れる：`pip install -r requirements-dev.txt`
      （本番デプロイは requirements.txt のみが使われる）
- [ ] migrate：`python manage.py migrate`
- [ ] 管理者作成：`python manage.py createsuperuser`
- [ ] quick_check：`./scripts/checks/quick_check.sh`
- [ ] 起動：`python manage.py runserver`
- [ ] ブランド名設定：`.env` に `SITE_NAME=<サービス名>` を追加
      （navbar / タイトル / フッターに反映される。未設定時は "SaaS Template"）
- [ ] デモデータ削除：`apps/app/views.py` の `_FAKE_CUSTOMERS` と
      customer_list / customer_create ビューはデモ実装。
      新サービスの機能実装時に削除するか、実モデルの queryset に置き換える

---

## 2) Stripe（当日中にやる）
- [ ] Product/Price 作成（月額980円 or サービスに合わせた価格）
- [ ] `STRIPE_SECRET_KEY` 設定
- [ ] `STRIPE_PRICE_ID` を `.env` に設定
- [ ] Webhook endpoint を作成
  - URL: `<SITE_URL>/stripe/webhook`
  - events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
- [ ] `STRIPE_WEBHOOK_SECRET` を `.env` に設定
- [ ] ローカルで課金導線確認
  - pricing → checkout → success
  - Stripe webhook が届き BillingProfile.status が active になる

---

## 3) 本番デプロイ（Railway）
- [ ] Railway にプロジェクト作成
- [ ] 環境変数を設定
  - `DEBUG=False`
  - `ALLOWED_HOSTS=<prod-domain>`
  - `SITE_URL=https://<prod-domain>`
  - `DATABASE_URL=<railway postgres URL>`
  - Stripe 本番キー一式（live）+ 本番Price ID + Webhook secret
- [ ] `python manage.py migrate` を本番で実行
- [ ] Stripe 本番Webhook endpoint 作成
  - URL: `https://<prod-domain>/stripe/webhook`
- [ ] 本番スモークテスト（RUNBOOKの項目を実施）

---

## 4) 2週間スプリント運用（テンプレ標準）
- [ ] Day 1-2: MVP最小機能（/app/ 直下）だけ作る
- [ ] Day 3-5: UI/動線・計測（最小のログ）・品質ゲート
- [ ] Day 6-7: リリース準備（README、利用規約/免責、運用メモ）
- [ ] Week 2: 改良 or 捨てる判断（課金/継続率/問い合わせを基準に）