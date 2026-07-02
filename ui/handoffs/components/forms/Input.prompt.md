Labeled text input — subtle border, blue focus ring. Pass `error` to switch the border/ring to red and show a message below.

```jsx
<Input label="夢のタイトル" placeholder="例: オーロラを見る" value={title} onChange={e => setTitle(e.target.value)} />
<Input label="メールアドレス" type="email" error="正しい形式で入力してください" />
```

Props: `label`, `hint`, `error`, plus any native `<input>` attribute (`type`, `placeholder`, `value`, `onChange`…).
