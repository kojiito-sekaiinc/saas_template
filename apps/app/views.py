from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def dashboard(request):
    """Main app dashboard (stub)."""
    return render(request, "app/dashboard.html")


# ---------------------------------------------------------------------------
# TODO(template): デモデータ — 新サービス作成時に削除・置換すること
#
# _FAKE_CUSTOMERS と customer_list / customer_create は UI デモ用の仮実装。
# 実サービスでは Customer モデルを実装して queryset に置き換えるか、
# 顧客一覧が不要なら該当ビューと apps/app/urls.py のルートを削除する。
# 手順は docs/TEMPLATE_CHECKLIST.md「1) 新規プロジェクト作成」を参照。
# ---------------------------------------------------------------------------
_FAKE_CUSTOMERS = [
    {"name": "Alice Kim",      "email": "alice@example.com",   "company": "Acme Corp",    "status": "Active",   "added": "Jan 12, 2025"},
    {"name": "Bob Tanaka",     "email": "bob@example.com",     "company": "Beta Ltd",     "status": "Active",   "added": "Feb  3, 2025"},
    {"name": "Carol Lee",      "email": "carol@example.com",   "company": "Gamma Inc",    "status": "Inactive", "added": "Feb 14, 2025"},
    {"name": "David Park",     "email": "david@example.com",   "company": "Delta Co",     "status": "Active",   "added": "Mar  1, 2025"},
    {"name": "Eve Yamamoto",   "email": "eve@example.com",     "company": "Epsilon LLC",  "status": "Active",   "added": "Mar  8, 2025"},
    {"name": "Frank Sato",     "email": "frank@example.com",   "company": "Zeta Corp",    "status": "Inactive", "added": "Mar 15, 2025"},
    {"name": "Grace Ito",      "email": "grace@example.com",   "company": "Eta Partners", "status": "Active",   "added": "Apr  2, 2025"},
    {"name": "Henry Nakamura", "email": "henry@example.com",   "company": "Theta Inc",    "status": "Active",   "added": "Apr 10, 2025"},
    {"name": "Iris Kobayashi", "email": "iris@example.com",    "company": "Iota Ltd",     "status": "Active",   "added": "Apr 18, 2025"},
    {"name": "Jack Suzuki",    "email": "jack@example.com",    "company": "Kappa Co",     "status": "Inactive", "added": "Apr 25, 2025"},
    {"name": "Karen Watanabe", "email": "karen@example.com",   "company": "Lambda LLC",   "status": "Active",   "added": "May  5, 2025"},
    {"name": "Leo Hayashi",    "email": "leo@example.com",     "company": "Mu Corp",      "status": "Active",   "added": "May 12, 2025"},
]


def _page_url(page_num, q, status):
    """ページ番号とフィルタパラメータから URL クエリ文字列を構築する。"""
    params = {"page": page_num}
    if q:
        params["q"] = q
    if status:
        params["status"] = status
    return "?" + urlencode(params)


def customer_list(request):
    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "")

    # --- フィルタ（仮データ用） ---
    customers = _FAKE_CUSTOMERS
    if q:
        q_lower = q.lower()
        customers = [
            c for c in customers
            if q_lower in c["name"].lower() or q_lower in c["email"].lower()
        ]
    if status_filter:
        customers = [
            c for c in customers
            if c["status"].lower() == status_filter.lower()
        ]

    total_count = len(customers)

    # --- ページネーション ---
    paginator = Paginator(customers, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    # --- table_rows 組み立て ---
    table_rows = [
        {
            "cells": [c["name"], c["email"], c["company"], c["status"], c["added"]],
            "actions": [
                {"label": "View", "url": "#"},
                {"label": "Edit", "url": "#"},
            ],
        }
        for c in page_obj
    ]

    # --- ページネーション URL（テンプレート側では組み立てない） ---
    prev_page_url = (
        _page_url(page_obj.previous_page_number, q, status_filter)
        if page_obj.has_previous else None
    )
    next_page_url = (
        _page_url(page_obj.next_page_number, q, status_filter)
        if page_obj.has_next else None
    )
    page_range_items = [
        {
            "number": n,
            "url": _page_url(n, q, status_filter),
            "is_current": n == page_obj.number,
        }
        for n in paginator.page_range
        if abs(n - page_obj.number) <= 2
    ]

    nav_items = [
        {"label": "Dashboard", "url": reverse("app:dashboard")},
        {"label": "Customers", "url": reverse("app:customer_list"), "active": True},
    ]

    return render(request, "customers/list.html", {
        "nav_items": nav_items,
        "table_headers": ["Name", "Email", "Company", "Status", "Added"],
        "table_rows": table_rows,
        "page_obj": page_obj,
        "search_query": q,
        "status_filter": status_filter,
        "total_count": total_count,
        "prev_page_url": prev_page_url,
        "next_page_url": next_page_url,
        "page_range_items": page_range_items,
    })


def customer_create(request):
    """Stub — Customer モデル実装後に置き換える。"""
    return HttpResponse("Coming soon", status=200)
