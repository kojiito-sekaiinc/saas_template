// Add/edit dream form + share-to-X modal.
const { useState: useSt } = React;

function ImageSlots({ images, onChange }) {
  const slots = [0, 1, 2, 3];
  return (
    <div>
      <label style={{ display: "block", fontSize: "var(--text-sm)", fontWeight: "var(--weight-medium)", color: "var(--color-text)", marginBottom: "var(--space-2)" }}>
        画像 <span style={{ color: "var(--color-text-subtle)", fontWeight: "var(--weight-normal)" }}>（最大4枚）</span>
      </label>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "var(--space-3)" }}>
        {slots.map((i) => {
          const src = images[i];
          return (
            <div key={i} onClick={() => onChange(i)} style={{
              aspectRatio: "1", borderRadius: "var(--radius-sm)", overflow: "hidden", cursor: "pointer",
              border: src ? "1px solid var(--color-border)" : "1px dashed var(--color-border-strong)",
              background: "var(--color-bg-subtle)", display: "flex", alignItems: "center", justifyContent: "center",
              color: "var(--color-text-subtle)", position: "relative",
            }}>
              {src ? (
                <img src={src} alt="" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function DreamForm({ dream, onCancel, onSave }) {
  const { Input, Textarea, Select, Button } = window.SekaiDesignSystem_2572f3;
  const [title, setTitle] = useSt(dream ? dream.title : "");
  const [desc, setDesc] = useSt(dream ? dream.desc : "");
  const [status, setStatus] = useSt(dream ? dream.status : "active");
  const [images, setImages] = useSt(dream ? dream.images.slice(0, 4) : []);
  const { PageHeader } = window;

  const toggleImg = (i) => {
    const next = images.slice();
    if (next[i]) next.splice(i, 1);
    else next[i] = `https://picsum.photos/seed/new${Date.now() % 1000}-${i}/640/480`;
    setImages(next.filter(Boolean));
  };

  return (
    <div style={{ maxWidth: 680, margin: "0 auto" }}>
      <PageHeader title={dream ? "夢を編集" : "新しい夢"} description="人生で叶えたいことを、ひとつ書き留めましょう。" />
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-6)" }}>
        <Input label="夢のタイトル" placeholder="例: オーロラを見る" value={title} onChange={(e) => setTitle(e.target.value)} />
        <Textarea label="夢の概要" maxLength={500} rows={5} value={desc} onChange={(e) => setDesc(e.target.value)}
          placeholder="この夢について、いまの気持ちを書いてみましょう。" />
        <Select label="ステータス" value={status} onChange={(e) => setStatus(e.target.value)}
          options={[{ value: "draft", label: "下書き" }, { value: "active", label: "進行中" }, { value: "done", label: "実現済み" }]} />
        <ImageSlots images={images} onChange={toggleImg} />
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "var(--space-3)", paddingTop: "var(--space-2)", borderTop: "1px solid var(--color-border)", marginTop: "var(--space-2)" }}>
          <Button variant="ghost" onClick={onCancel}>キャンセル</Button>
          <Button variant="primary" onClick={() => onSave({ title, desc, status, images })} disabled={!title.trim()}>
            {dream ? "保存" : "夢を追加"}
          </Button>
        </div>
      </div>
    </div>
  );
}

function ShareModal({ dream, onClose }) {
  const { Button, Badge } = window.SekaiDesignSystem_2572f3;
  const { Icon, ICONS } = window;
  const text = `私の夢 #${dream.n}「${dream.title}」 — Sekai で叶えたい夢を記録中。`;
  return (
    <div onClick={onClose} style={{
      position: "fixed", inset: 0, zIndex: 50, background: "rgba(25,25,25,0.4)",
      display: "flex", alignItems: "center", justifyContent: "center", padding: "var(--space-6)",
    }}>
      <div onClick={(e) => e.stopPropagation()} style={{
        width: "100%", maxWidth: 460, background: "var(--color-surface)", border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-sm)", overflow: "hidden",
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "var(--space-5) var(--space-6)", borderBottom: "1px solid var(--color-border)" }}>
          <h2 style={{ fontSize: "var(--text-lg)", fontWeight: "var(--weight-semibold)", color: "var(--color-text)" }}>夢をシェア</h2>
          <button onClick={onClose} aria-label="閉じる" style={{ width: 28, height: 28, display: "inline-flex", alignItems: "center", justifyContent: "center", border: "none", background: "transparent", color: "var(--color-text-muted)", cursor: "pointer", borderRadius: "var(--radius-sm)" }}>
            <Icon path={ICONS.x} size={18} />
          </button>
        </div>
        <div style={{ padding: "var(--space-6)" }}>
          <div style={{ border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)", padding: "var(--space-4)", marginBottom: "var(--space-5)" }}>
            {dream.images[0] ? (
              <div style={{ aspectRatio: "16/9", borderRadius: "var(--radius-sm)", overflow: "hidden", marginBottom: "var(--space-3)" }}>
                <img src={dream.images[0]} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
              </div>
            ) : null}
            <p style={{ fontSize: "var(--text-sm)", color: "var(--color-text)", lineHeight: "var(--leading-relaxed)" }}>{text}</p>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--color-primary)" }}>sekai.app/d/{dream.id}</span>
          </div>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "var(--space-3)" }}>
            <Button variant="secondary" onClick={onClose}>リンクをコピー</Button>
            <Button variant="primary" onClick={onClose} iconLeft={<Icon path={ICONS.x} fill size={14} />}>X に投稿</Button>
          </div>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { DreamForm, ShareModal });
