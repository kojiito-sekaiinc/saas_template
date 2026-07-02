Primary action button — flat fills, subtle borders, fast color-only hover. Use at most one `primary` per view section; everything else is `secondary`, `ghost`, or `danger`.

```jsx
<Button variant="primary" onClick={save}>夢を保存</Button>
<Button variant="secondary">キャンセル</Button>
<Button variant="ghost" size="sm">すべて表示</Button>
<Button variant="danger">削除</Button>
```

Variants: `primary` (blue fill, sparingly), `secondary` (white + border), `ghost` (transparent), `danger` (red text on white). Sizes: `sm` / `md` / `lg`. Pass `iconLeft` / `iconRight` for 16px icons, `as="a"` + `href` for links.
