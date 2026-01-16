from django.shortcuts import render


def dashboard(request):
    """Main app dashboard (stub)."""
    return render(request, "app/dashboard.html")
