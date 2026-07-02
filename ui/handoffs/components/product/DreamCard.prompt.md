The core unit of the Sekai Dreams app. Shows a cover mosaic (up to 4 images in a 1 + 3 layout, extras become a "+N" overlay), title, 2-line description, a status badge (`下書き`/`進行中`/`実現済み`), and a Share-to-X button. Falls back to a calm placeholder when no images.

```jsx
<DreamCard
  index={7}
  title="オーロラを見る"
  description="アイスランドかノルウェーで、冬の夜空を埋めるオーロラを自分の目で見る。"
  images={["/a.jpg","/b.jpg","/c.jpg","/d.jpg"]}
  status="active"
  onShare={() => shareToX(dream)}
  onClick={() => openDream(dream)}
/>
```

Status maps to Badge tone: draft→neutral, active→primary, done→success. Designed for a responsive grid (min card ~300px).
