import React from "react";

const SIZES = { sm: 28, md: 36, lg: 48 };

/**
 * User avatar — image when `src` is set, otherwise initials on a subtle fill.
 */
export function Avatar({ src, name = "", size = "md", className = "", style = {}, ...props }) {
  const px = typeof size === "number" ? size : SIZES[size] || SIZES.md;
  const initials = name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0])
    .join("")
    .toUpperCase();
  return (
    <span
      className={className}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        width: px,
        height: px,
        borderRadius: "var(--radius-full)",
        background: "var(--color-bg-subtle)",
        border: "1px solid var(--color-border)",
        color: "var(--color-text-muted)",
        fontSize: Math.max(11, Math.round(px * 0.36)),
        fontWeight: "var(--weight-medium)",
        overflow: "hidden",
        flexShrink: 0,
        ...style,
      }}
      {...props}
    >
      {src ? (
        <img src={src} alt={name} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        initials || "?"
      )}
    </span>
  );
}
