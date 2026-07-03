"""
E2E テスト専用の pytest 設定。

pytest-playwright は sync API でも内部で asyncio イベントループを保持するため、
Django が「async コンテキストからの ORM 呼び出し」と誤検知して
SynchronousOnlyOperation を投げる。E2E テストは実際には同期実行なので、
Playwright 公式ドキュメントの推奨に従い許可する。

この設定は tests/e2e 配下の実行時のみ読み込まれる（通常の pytest には影響しない）。
"""
import os

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
