// App shell — topbar + sidebar for the Sekai Dreams app.
const { useState } = React;

function Icon({ path, fill = false, size = 16, stroke = 1.5 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24"
      fill={fill ? "currentColor" : "none"} stroke={fill ? "none" : "currentColor"}
      strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {path}
    </svg>
  );
}
const ICONS = {
  home: <path d="M2.25 12l8.954-8.955a1.126 1.126 0 011.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75" />,
  star: <path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />,
  check: <path d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />,
  doc: <path d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />,
  settings: <path d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />,
  plus: <path d="M12 4.5v15m7.5-7.5h-15" />,
  search: <path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />,
  bell: <path d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />,
  back: <path d="M15.75 19.5L8.25 12l7.5-7.5" />,
  x: <path d="M6 18L18 6M6 6l12 12" />,
};

function NavItem({ icon, label, badge, active, onClick }) {
  const [hover, setHover] = useState(false);
  return (
    <a onClick={onClick} onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        display: "flex", alignItems: "center", gap: "var(--space-2)",
        padding: "6px 8px", fontSize: "var(--text-sm)", borderRadius: "var(--radius-sm)",
        cursor: "pointer", transition: "background-color var(--duration-fast) var(--ease)",
        color: active ? "var(--color-primary)" : "var(--color-text-muted)",
        fontWeight: active ? "var(--weight-medium)" : "var(--weight-normal)",
        background: active ? "var(--color-bg-subtle)" : hover ? "var(--color-surface-hover)" : "transparent",
      }}>
      <span style={{ flexShrink: 0, width: 16, height: 16, display: "inline-flex" }}>
        <Icon path={icon} stroke={active ? 1.8 : 1.5} />
      </span>
      <span style={{ flex: 1 }}>{label}</span>
      {badge != null ? (
        <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-subtle)", fontVariantNumeric: "tabular-nums" }}>{badge}</span>
      ) : null}
    </a>
  );
}

function AppShell({ active, onNav, onAdd, children }) {
  const { Avatar, Button } = window.SekaiDesignSystem_2572f3;
  const nav = [
    { key: "dreams", icon: ICONS.home, label: "すべての夢", badge: 9 },
    { key: "active", icon: ICONS.star, label: "進行中", badge: 4 },
    { key: "done", icon: ICONS.check, label: "実現済み", badge: 3 },
    { key: "draft", icon: ICONS.doc, label: "下書き", badge: 2 },
  ];
  return (
    <div style={{ minHeight: "100vh", background: "var(--color-bg)" }}>
      {/* Topbar */}
      <header style={{
        position: "sticky", top: 0, zIndex: 20, height: "var(--layout-header-height)",
        background: "var(--color-surface)", borderBottom: "1px solid var(--color-border)",
        display: "flex", alignItems: "center",
      }}>
        <div style={{
          width: "var(--layout-sidebar-width)", height: "100%", flexShrink: 0,
          display: "flex", alignItems: "center", gap: 10, padding: "0 var(--space-6)",
          borderRight: "1px solid var(--color-border)",
        }}>
          <span style={{ width: 20, height: 20, borderRadius: "var(--radius-full)", background: "var(--color-primary)", display: "inline-flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
            <span style={{ width: 7, height: 7, borderRadius: "var(--radius-full)", background: "#fff" }} />
          </span>
          <span style={{ fontSize: "var(--text-md)", fontWeight: "var(--weight-semibold)", letterSpacing: "-0.02em", color: "var(--color-text)" }}>Sekai</span>
        </div>
        <div style={{ flex: 1, display: "flex", alignItems: "center", padding: "0 var(--space-6)" }}>
          <div style={{ position: "relative", width: "100%", maxWidth: 360 }}>
            <span style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", color: "var(--color-text-subtle)", display: "inline-flex" }}>
              <Icon path={ICONS.search} size={15} />
            </span>
            <input placeholder="夢を検索" style={{
              width: "100%", padding: "7px 12px 7px 32px", fontSize: "var(--text-sm)", fontFamily: "var(--font-sans)",
              color: "var(--color-text)", background: "var(--color-bg-subtle)", border: "1px solid var(--color-border)",
              borderRadius: "var(--radius-sm)", outline: "none",
            }} />
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", padding: "0 var(--space-6)" }}>
          <button aria-label="通知" style={{ width: 32, height: 32, display: "inline-flex", alignItems: "center", justifyContent: "center", borderRadius: "var(--radius-sm)", border: "none", background: "transparent", color: "var(--color-text-muted)", cursor: "pointer" }}>
            <Icon path={ICONS.bell} />
          </button>
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", paddingLeft: "var(--space-3)", borderLeft: "1px solid var(--color-border)" }}>
            <Avatar name="Koji Ito" size="sm" />
            <span style={{ fontSize: "var(--text-sm)", color: "var(--color-text)" }}>Koji</span>
          </div>
        </div>
      </header>

      <div style={{ display: "flex", minHeight: "calc(100vh - var(--layout-header-height))" }}>
        {/* Sidebar */}
        <aside style={{
          width: "var(--layout-sidebar-width)", flexShrink: 0, background: "var(--color-bg-subtle)",
          borderRight: "1px solid var(--color-border)", display: "flex", flexDirection: "column",
          position: "sticky", top: "var(--layout-header-height)", height: "calc(100vh - var(--layout-header-height))",
        }}>
          <div style={{ padding: "var(--space-4)" }}>
            <Button variant="primary" size="md" onClick={onAdd}
              iconLeft={<Icon path={ICONS.plus} />} style={{ width: "100%" }}>
              夢を追加
            </Button>
          </div>
          <nav style={{ display: "flex", flexDirection: "column", gap: 2, padding: "0 var(--space-3)", flex: 1 }}>
            {nav.map((n) => (
              <NavItem key={n.key} icon={n.icon} label={n.label} badge={n.badge}
                active={active === n.key} onClick={() => onNav(n.key)} />
            ))}
            <div style={{ margin: "var(--space-2) 8px", borderTop: "1px solid var(--color-border)" }} />
            <NavItem icon={ICONS.settings} label="設定" active={active === "settings"} onClick={() => onNav("settings")} />
          </nav>
          <div style={{ padding: "var(--space-4) var(--space-5)", borderTop: "1px solid var(--color-border)" }}>
            <a style={{ fontSize: "var(--text-xs)", color: "var(--color-text-muted)", cursor: "pointer" }}>サインアウト</a>
          </div>
        </aside>

        {/* Main */}
        <main style={{ flex: 1, minWidth: 0, overflowY: "auto" }}>
          <div style={{ maxWidth: "var(--layout-content-max-width)", margin: "0 auto", padding: "var(--space-8)" }}>
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

Object.assign(window, { AppShell, Icon, ICONS });
