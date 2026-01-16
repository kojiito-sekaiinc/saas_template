# SaaS Template

A reusable Django template for building SaaS applications.

This template is designed for rapid SaaS development with a fixed technology stack and subscription-based billing.

## Technology Stack

- **Backend**: Django
- **Frontend**: Django Templates + HTMX + Tailwind CSS (static)
- **Database**: Supabase PostgreSQL (SQLite for local development)
- **Payments**: Stripe (subscription model)
- **Deployment**: Railway
- **Static Files**: WhiteNoise

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

5. Start the development server:

```bash
python manage.py runserver
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes (production) |
| `DEBUG` | Debug mode (True/False) | No (default: True) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No |
| `DATABASE_URL` | PostgreSQL connection URL | No (uses SQLite if empty) |
| `STRIPE_SECRET_KEY` | Stripe secret API key | Yes (for billing) |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable API key | Yes (for billing) |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | Yes (for billing) |
| `STRIPE_PRICE_ID` | Stripe Price ID for subscription | Yes (for billing) |

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
