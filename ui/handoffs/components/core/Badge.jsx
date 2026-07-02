import React from "react";

const TONES = {
  neutral: { color: "var(--color-text-muted)", background: "var(--color-bg-subtle)", border: "var(--color-border)" },
  primary: { color: "var(--color-primary)", background: "var(--color-primary-subtle)", border: "transparent" },
  success: { color: "var(--color-success)", background: "var(--color-success-subtle)", border: "transparent" },
  warning: { color: "var(--color-warning)", background: "var(--color-warning-subtle)", border: "transparent" },
  danger: { color: "var(--color-danger)", background: "var(--color-danger-subtle)", border: "transparent" },
};

/**
 * Small status/label pill. Optional leading dot for state indicators.
 */
export function Badge({ children, tone = "neutral", dot = false, className = "", style = {}, ...props }) {
  const t = TONES[tone] || TONES.neutral;
  return (
    <span
      className={className}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "var(--space-2)",
        padding: "2px 8px",
        fontSize: "var(--text-xs)",
        fontWeight: "var(--weight-medium)",
        lineHeight: "var(--leading-normal)",
        color: t.color,
        background: t.background,
        border: `1px solid ${t.border}`,
        borderRadius: "var(--radius-sm)",
        whiteSpace: "nowrap",
        ...style,
      }}
      {...props}
    >
      {dot ? (
        <span style={{ width: 6, height: 6, borderRadius: "var(--radius-full)", background: "currentColor", flexShrink: 0 }} />
      ) : null}
      {children}
    </span>
  );
}
