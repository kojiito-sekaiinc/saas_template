"""
conftest.py — プロジェクト共通フィクスチャ

【フィクスチャ/ファクトリの方針】

1. テストランナー
   - pytest 統一。django.test.TestCase は使用しない。
   - DB アクセスには @pytest.mark.django_db または db/django_db_setup フィクスチャ。

2. フィクスチャの配置ルール
   - このファイル (conftest.py): 複数モジュールで共用するフィクスチャのみ。
   - 各テストモジュール: そのモジュール固有のフィクスチャ（@pytest.fixture をモジュール先頭に定義）。

3. ファクトリパターン
   - 単純なオブジェクト生成は User.objects.create_user() 等を直接呼ぶ。
   - 複数テストで引数違いのオブジェクトを生成する場合は make_user のようなファクトリフィクスチャを使う。
   - factory_boy 等の外部ファクトリライブラリは導入しない（現時点では不要）。

4. 設定のオーバーライド
   - テスト単位の設定変更は @override_settings(KEY=value) を関数デコレータとして使う。
   - 複数テストに共通する設定変更は autouse=True フィクスチャで settings.KEY = value で行う。

5. モック
   - Stripe 等の外部 API は unittest.mock.patch() でモックする。
   - pytest monkeypatch フィクスチャも可（settings の一時変更に便利）。
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def make_user(db):
    """
    任意の属性でユーザーを生成するファクトリフィクスチャ。

    使用例:
        def test_something(make_user):
            user = make_user()                              # デフォルト
            admin = make_user(email="admin@example.com")   # カスタム
    """
    def _make(email="test@example.com", password="TestPass1!", **kwargs):
        return User.objects.create_user(email=email, password=password, **kwargs)
    return _make
