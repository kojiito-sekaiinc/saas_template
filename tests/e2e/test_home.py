"""
E2E smoke test — ホームページが実ブラウザで描画されることを確認する。

実行方法（通常の pytest からは分離されている。pytest.ini の testpaths 参照）:

    playwright install chromium   # 初回のみ
    pytest tests/e2e

サーバは pytest-django の live_server フィクスチャが起動するため、
runserver を別途立てる必要はない。
"""


def test_home_page(page, live_server):
    page.goto(live_server.url)

    assert page.title() != ""
