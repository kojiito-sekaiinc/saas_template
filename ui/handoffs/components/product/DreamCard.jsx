import React from "react";
import { Badge } from "../core/Badge.jsx";

const STATUS = {
  draft: { tone: "neutral", label: "下書き" },
  active: { tone: "primary", label: "進行中" },
  done: { tone: "success", label: "実現済み" },
};

function ShareIcon() {
  // X (formerly Twitter) glyph
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  );
}

function Placeholder() {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--color-bg-subtle)",
        color: "var(--color-text-subtle)",
      }}
    >
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M21 15l-5-5L5 21" />
      </svg>
    </div>
  );
}

/**
 * Dream card — the core unit of the Sekai Dreams app. Cover image (up to 4,
 * shown as a 1 + 3 mosaic), title, description excerpt, status badge, and a
 * Share-to-X action. Composes Badge.
 */
export function DreamCard({
  title,
  description,
  images = [],
  status = "active",
  index,
  onShare,
  onClick,
  className = "",
  style = {},
  ...props
}) {
  const [hover, setHover] = React.useState(false);
  const s = STATUS[status] || STATUS.active;
  const imgs = images.slice(0, 4);
  const extra = images.length - 4;

  return (
    <div
      className={className}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={onClick}
      style={{
        background: "var(--color-surface)",
        border: "1px solid",
        borderColor: hover ? "var(--color-border-strong)" : "var(--color-border)",
        borderRadius: "var(--radius-md)",
        overflow: "hidden",
        cursor: onClick ? "pointer" : "default",
        display: "flex",
        flexDirection: "column",
        transition: "border-color var(--duration-base) var(--ease)",
        ...style,
      }}
      {...props}
    >
      {/* Cover mosaic */}
      <div style={{ position: "relative", aspectRatio: "16 / 10", background: "var(--color-bg-subtle)" }}>
        {imgs.length === 0 ? (
          <Placeholder />
        ) : imgs.length === 1 ? (
          <img src={imgs[0]} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gridTemplateRows: "1fr 1fr", gap: 2, height: "100%" }}>
            <img src={imgs[0]} alt="" style={{ gridRow: "1 / 3", width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
            {imgs.slice(1, 4).map((src, i) => (
              <div key={i} style={{ position: "relative", overflow: "hidden" }}>
                <img src={src} alt="" style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }} />
                {i === 2 && extra > 0 ? (
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      background: "rgba(25,25,25,0.55)",
                      color: "#fff",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "var(--text-sm)",
                      fontWeight: "var(--weight-medium)",
                    }}
                  >
                    +{extra}
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        )}
        <div style={{ position: "absolute", top: "var(--space-3)", left: "var(--space-3)" }}>
          <Badge tone={s.tone} dot style={{ background: "rgba(255,255,255,0.92)", backdropFilter: "blur(4px)" }}>
            {s.label}
          </Badge>
        </div>
      </div>

      {/* Body */}
      <div style={{ padding: "var(--space-4)", display: "flex", flexDirection: "column", gap: "var(--space-2)", flex: 1 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-2)" }}>
          {index != null ? (
            <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-subtle)", fontVariantNumeric: "tabular-nums", flexShrink: 0 }}>
              #{index}
            </span>
          ) : null}
          <h3
            style={{
              fontSize: "var(--text-md)",
              fontWeight: "var(--weight-semibold)",
              color: "var(--color-text)",
              lineHeight: "var(--leading-tight)",
              margin: 0,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {title}
          </h3>
        </div>
        {description ? (
          <p
            style={{
              fontSize: "var(--text-sm)",
              color: "var(--color-text-muted)",
              lineHeight: "var(--leading-relaxed)",
              margin: 0,
              display: "-webkit-box",
              WebkitLineClamp: 2,
              WebkitBoxOrient: "vertical",
              overflow: "hidden",
            }}
          >
            {description}
          </p>
        ) : null}

        <div style={{ marginTop: "auto", paddingTop: "var(--space-3)", display: "flex", justifyContent: "flex-end" }}>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onShare && onShare();
            }}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "var(--space-2)",
              padding: "4px 10px",
              fontSize: "var(--text-xs)",
              fontWeight: "var(--weight-medium)",
              color: "var(--color-text-muted)",
              background: "transparent",
              border: "1px solid var(--color-border)",
              borderRadius: "var(--radius-sm)",
              cursor: "pointer",
              transition: "background-color var(--duration-base) var(--ease), color var(--duration-base) var(--ease)",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "var(--color-surface-hover)";
              e.currentTarget.style.color = "var(--color-text)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "transparent";
              e.currentTarget.style.color = "var(--color-text-muted)";
            }}
          >
            <ShareIcon />
            シェア
          </button>
        </div>
      </div>
    </div>
  );
}
