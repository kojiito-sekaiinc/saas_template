Native select styled to match `Input` — label, custom chevron, blue focus ring. `options` takes plain strings or `{value,label}` objects.

```jsx
<Select label="並び替え" value={sort} onChange={e => setSort(e.target.value)}
  options={[{value:"recent",label:"最近追加"},{value:"progress",label:"進捗順"}]} />
```
