// Dream grid (list view), detail, form, and share modal screens.
const { useState: useS } = React;

function PageHeader({ title, description, action }) {
  return (
    <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "var(--space-4)", marginBottom: "var(--space-6)" }}>
      <div>
        <h1 style={{ fontSize: "var(--text-xl)", fontWeight: "var(--weight-semibold)", color: "var(--color-text)", lineHeight: "var(--leading-tight)", letterSpacing: "-0.01em" }}>{title}</h1>
        {description ? <p style={{ marginTop: 6, fontSize: "var(--text-sm)", color: "var(--color-text-muted)" }}>{description}</p> : null}
      </div>
      {action}
    </div>
  );
}

function DreamGrid({ dreams, filter, onOpen, onShare, onAdd, onFilterChange }) {
  const { DreamCard, ProgressBar, Button, Select } = window.SekaiDesignSystem_2572f3;
  const { Icon, ICONS } = window;
  const list = filter === "dreams" ? dreams : dreams.filter((d) => d.status === ({ active: "active", done: "done", draft: "draft" }[filter]));
  const doneCount = dreams.filter((d) => d.status === "done").length;
  const titles = { dreams: "すべての夢", active: "進行中", done: "実現済み", draft: "下書き" };
  const descs = {
    dreams: "あなたが人生で叶えたい夢。最大100件まで登録できます。",
    active: "いま動き出している夢。", done: "もう叶えた夢。おめでとう。", draft: "まだ書きかけの夢。",
  };

  return (
    <div>
      <PageHeader title={titles[filter]} description={descs[filter]}
        action={<Button variant="primary" size="md" onClick={onAdd} iconLeft={<Icon path={ICONS.plus} />}>夢を追加</Button>} />

      {filter === "dreams" ? (
        <div style={{ background: "var(--color-surface)", border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)", padding: "var(--space-5) var(--space-6)", marginBottom: "var(--space-6)", display: "flex", alignItems: "center", gap: "var(--space-8)", flexWrap: "wrap" }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-2)" }}>
            <span style={{ fontSize: 32, fontWeight: "var(--weight-semibold)", color: "var(--color-text)", lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{doneCount}</span>
            <span style={{ fontSize: "var(--text-sm)", color: "var(--color-text-muted)" }}>/ {window.TOTAL} 実現</span>
          </div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <ProgressBar value={doneCount} max={window.TOTAL} label="人生の進捗" showValue />
          </div>
        </div>
      ) : null}

      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-4)" }}>
        <span style={{ fontSize: "var(--text-sm)", color: "var(--color-text-muted)" }}>{list.length} 件の夢</span>
        <div style={{ width: 160 }}>
          <Select value={filter} onChange={(e) => onFilterChange(e.target.value)}
            options={[{ value: "dreams", label: "すべて表示" }, { value: "active", label: "進行中のみ" }, { value: "done", label: "実現済みのみ" }, { value: "draft", label: "下書きのみ" }]} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "var(--space-5)" }}>
        {list.map((d) => (
          <DreamCard key={d.id} index={d.n} title={d.title} description={d.desc}
            images={d.images} status={d.status} onClick={() => onOpen(d)} onShare={() => onShare(d)} />
        ))}
      </div>
    </div>
  );
}

function DreamDetail({ dream, onBack, onShare, onEdit }) {
  const { Badge, Button } = window.SekaiDesignSystem_2572f3;
  const { Icon, ICONS } = window;
  const [active, setActive] = useS(0);
  const STATUS = { draft: ["neutral", "下書き"], active: ["primary", "進行中"], done: ["success", "実現済み"] };
  const s = STATUS[dream.status];
  const imgs = dream.images;

  return (
    <div>
      <button onClick={onBack} style={{ display: "inline-flex", alignItems: "center", gap: 6, fontSize: "var(--text-sm)", color: "var(--color-text-muted)", background: "transparent", border: "none", cursor: "pointer", marginBottom: "var(--space-5)", padding: 0 }}>
        <Icon path={ICONS.back} size={15} /> すべての夢
      </button>

      <div style={{ display: "grid", gridTemplateColumns: imgs.length ? "1.3fr 1fr" : "1fr", gap: "var(--space-8)", alignItems: "start" }}>
        {imgs.length ? (
          <div>
            <div style={{ aspectRatio: "4 / 3", borderRadius: "var(--radius-lg)", overflow: "hidden", border: "1px solid var(--color-border)", background: "var(--color-bg-subtle)" }}>
              <img src={imgs[active]} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
            </div>
            {imgs.length > 1 ? (
              <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "var(--space-3)" }}>
                {imgs.map((src, i) => (
                  <button key={i} onClick={() => setActive(i)} style={{
                    width: 64, height: 64, borderRadius: "var(--radius-sm)", overflow: "hidden", padding: 0, cursor: "pointer",
                    border: `2px solid ${i === active ? "var(--color-primary)" : "var(--color-border)"}`, background: "none",
                  }}>
                    <img src={src} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
                  </button>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}

        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginBottom: "var(--space-3)" }}>
            <Badge tone={s[0]} dot>{s[1]}</Badge>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-subtle)", fontVariantNumeric: "tabular-nums" }}>夢 #{dream.n}</span>
          </div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: "var(--weight-semibold)", color: "var(--color-text)", lineHeight: "var(--leading-tight)", marginBottom: "var(--space-4)" }}>{dream.title}</h1>
          <p style={{ fontSize: "var(--text-md)", color: "var(--color-text-muted)", lineHeight: "var(--leading-relaxed)", marginBottom: "var(--space-6)" }}>{dream.desc || "まだ概要が書かれていません。"}</p>
          <div style={{ display: "flex", gap: "var(--space-3)" }}>
            <Button variant="primary" onClick={() => onShare(dream)} iconLeft={<Icon path={ICONS.x} fill size={14} />}>X でシェア</Button>
            <Button variant="secondary" onClick={onEdit}>編集</Button>
          </div>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { DreamGrid, DreamDetail, PageHeader });
