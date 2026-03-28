**sync_billing_from_stripe 実装仕様書**


## **目的**
  
Stripe Webhook に依存している現在の課金状態同期に対して、

**Webhook未達・障害時でも整合性を回復できる手段を提供する**

  

そのために以下を実装する：

- Stripeを正本とした BillingProfile 再同期機能
    
- management command による手動実行機構
    
- dry-run による安全な差分確認
    

---

## **前提**

  

既存テンプレートには以下が存在する：

- BillingProfile
    
    - stripe_customer_id
        
    - stripe_subscription_id
        
    - status
        
    - current_period_end
        
    - last_stripe_event_created（※更新しない）
        
    
- Webhookによる状態更新ロジック（正本）
    

---

## **非目的（重要）**

  

以下は今回の実装対象外：

- Stripe側の状態変更
    
- Webhookロジックの変更
    
- last_stripe_event_created の更新
    
- 複数プラン対応
    

---

## **実装概要**

  

以下の2つを追加する：

  

### **1. services.py**

  

責務：

- Stripeから現在状態を取得
    
- BillingProfileに反映
    
- 差分を算出
    

  

関数：

  

#### **get_stripe_billing_state**

入力：

- subscription_id（optional）
    
- customer_id（optional）
    
- expected_price_id（required）
    

  

処理：

1. subscription_id があれば最優先で取得
    
2. なければ customer_id から subscription一覧取得
    
3. expected_price_id に一致する subscription を抽出
    
4. 最適な1件を選択
    
5. 状態を正規化して返す
    

  

出力：
```
{
  found: bool,
  stripe_customer_id: str | None,
  stripe_subscription_id: str | None,
  status: str,
  current_period_end: datetime | None,
  source: "subscription_id" | "customer_id" | "none"
}
```

#### **diff_billing_profile**

BillingProfileとStripe状態の差分を返す

---

#### **apply_stripe_state_to_billing_profile**

注意：

- last_stripe_event_created は更新しない
    

  

更新対象：

- stripe_customer_id
    
- stripe_subscription_id
    
- status
    
- current_period_end
    

---

#### **sync_billing_profile_from_stripe**

処理：

- select_for_updateでロック
    
- Stripe状態取得
    
- 差分算出
    
- 差分があれば更新（dry-run時は更新しない）
    

---

### **2. management command**


```
ファイル：
apps/billing/management/commands/sync_billing_from_stripe.py
```
## **コマンド仕様**

### **引数**
```

--user-id
--email
--all
--dry-run

```

制約：

- 上記のうち1つのみ指定可能
    

---

### **動作**

#### **単一ユーザー**

- BillingProfile取得 or 作成
    
- Stripeと同期
    

  

#### **全件**

- 全BillingProfileを対象
    

---

### **出力形式**

  

JSONで1行ずつ出力：

例：
```
UPDATED {"user_id":1,"email":"a@example.com","diffs":{...}}
NO_CHANGE {"user_id":2,...}
ERROR user_id=3 ...

```
### **dry-run**

- DB更新しない
    
- WOULD_UPDATE として出力
    

---

## **ログ出力**

  

最低限：

- user_id
    
- email
    
- stripe_customer_id
    
- stripe_subscription_id
    
- status変更
    
- source
    

---

## **エラーハンドリング**

- Stripe APIエラーはログ出力
    
- 他ユーザー処理は継続
    

---

## **実装上の注意**

- Stripe API key は settings から取得
    
- STRIPE_PRICE_ID を必ず使用
    
- last_stripe_event_created は絶対に触らない
    
- subscriptionが見つからない場合は not_subscribed
    

---

## **受け入れ条件**

  

以下が満たされること：

- 単一ユーザー同期が成功する
    
- dry-runで差分が確認できる
    
- subscription_id 不正でも customer_id から復元できる
    
- DB更新後、Paywall判定が正しく動く
    
- last_stripe_event_created が変更されない
    

---

## **完了後にやること**

- RUNBOOK.md に手順追記
    
- テスト追加（最低限）