# Sekai UI System 更新 → SaaS Template 反映手順

このドキュメントは、**Sekai UI System を更新した際に SaaS Template
へ安全に反映するための標準手順**をまとめたものです。

目的：

-   UI System の更新を SaaS Template に反映する
-   既存テンプレートの破壊を防ぐ
-   AI を使って **影響分析 → 最小修正** を行う

------------------------------------------------------------------------

# 全体フロー

1.  UI System更新\
2.  SaaS Templateの `ui/` を更新\
3.  AIに影響分析させる\
4.  AIに最小修正させる\
5.  人間が動作確認\
6.  commit / push

この順番を **必ず守る**。

------------------------------------------------------------------------

# 1. Sekai UI System を更新

Sekai UI System 側で以下を更新する。

    ui/
     ├ design/
     ├ components/
     ├ layouts/
     └ examples/

例

-   コンポーネント改善
-   layout 改修
-   design tokens 変更
-   Tailwind config 更新

更新後、**UI System が正常に動作することを確認する。**

------------------------------------------------------------------------

# 2. SaaS Template の `ui/` を更新

SaaS Template 側の `ui/` ディレクトリを更新する。

例

    project-root/
     ├ ui/
     │  ├ components/
     │  ├ layouts/
     │  ├ design/
     │  └ examples/

方法

    Sekai UI System → SaaS Template
    ui/ を丸ごとコピー

この段階では **まだテンプレート修正は行わない。**

------------------------------------------------------------------------

# 3. AI に影響分析させる

Claude / GPT に **影響分析のみ**させる。

目的

-   破壊的変更の検出
-   コンポーネント API 変更の検出
-   レイアウト block 変更の検出
-   テンプレート破損の可能性検出

AI には次を禁止する。

    Do NOT modify files
    Do NOT rewrite templates
    Analysis only

------------------------------------------------------------------------

# 4. AI に最小修正させる

影響分析結果を元に **必要最小限の修正のみ**適用する。

AI に必ず守らせるルール

    - redesign禁止
    - template全面書き換え禁止
    - unrelated変更禁止
    - minimal change only

------------------------------------------------------------------------

# 5. 人間による動作確認

最低限次を確認する。

## 画面確認

-   sidebar
-   header
-   table
-   form
-   pagination

## モバイル確認

-   sidebar drawer
-   hamburger menu

## Djangoエラー確認

-   NoReverseMatch
-   TemplateSyntaxError
-   Missing context variables

------------------------------------------------------------------------

# 6. Git commit

問題なければ commit する。

``` bash
git add .
git commit -m "Update Sekai UI System compatibility"
git push origin main
```

------------------------------------------------------------------------

# AI 更新フローのメリット

## ① UI 更新が安全になる

AIが

-   破壊的変更
-   API変更
-   template破壊

を検出できる。

------------------------------------------------------------------------

## ② AIが暴走しない

AIはよく

-   UIを全部書き直す
-   designを変更する
-   logicを壊す

ことがある。

この手順では

    影響分析
    ↓
    最小修正

を分離することで防止できる。

------------------------------------------------------------------------

## ③ UI System を進化させやすい

Sekai UI System を

-   大幅改善
-   layout変更
-   component改善

しても、

**SaaS Template 側で安全に更新できる。**

------------------------------------------------------------------------

# よくある事故

## AIがUIを全部書き直す

原因

    影響分析をせずに修正させる

対策

    必ず Impact Analysis → Minimal Fix

------------------------------------------------------------------------

## pagination URL が壊れる

原因

    テンプレートでURL組み立て

対策

    viewでURL生成

------------------------------------------------------------------------

## table actions 列が消える

原因

    show_actions=True を渡していない

------------------------------------------------------------------------

# 推奨ディレクトリ構成

    project
     ├ ui
     │  ├ design
     │  ├ components
     │  ├ layouts
     │  └ examples
     │
     ├ templates
     │  ├ customers
     │  ├ accounts
     │  └ billing
     │
     └ apps

------------------------------------------------------------------------

# 将来の改善（任意）

## select コンポーネント統一

    components/select.html

------------------------------------------------------------------------

## UI regression テスト

Playwright などで

    UI screenshot diff

------------------------------------------------------------------------

## UI versioning

    ui_version = "1.3.0"

------------------------------------------------------------------------

# まとめ

Sekai UI System 更新時は

    UI更新
    ↓
    ui/コピー
    ↓
    AI影響分析
    ↓
    AI最小修正
    ↓
    人間確認
    ↓
    commit

この運用を徹底することで

-   UI System を高速に進化させながら
-   SaaS Template を安全に保守

できる。
