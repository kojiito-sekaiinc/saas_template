Multi-line input with label, hint/error, and an optional character counter. Pass `maxLength` to show a live `n / max` counter (used for dream descriptions).

```jsx
<Textarea label="夢の概要" maxLength={500} rows={5}
  value={desc} onChange={e => setDesc(e.target.value)}
  placeholder="この夢について書いてみましょう" />
```
