import React from "react";

/**
 * Thin progress bar for dream completion. Calm — blue fill on a subtle track,
 * optional inline label + percentage.
 */
export function ProgressBar({
  value = 0,
  max = 100,
  label,
  showValue = false,
  tone = "primary",
  className = "",
  style = {},
  ...props
}) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100));
  const fill = {
    primary: "var(--color-primary)",
    success: "var(--color-success)",
    neutral: "var(--color-text-subtle)",
  }[tone] || "var(--color-primary)";

  return (
    <div className={className} style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)", ...style }} {...props}>
      {label || showValue ? (
        <div style={{ display: "flex", justifyContent: "space-between", gap: "var(--space-3)" }}>
          {label ? (
            <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-muted)" }}>{label}</span>
          ) : <span />}
          {showValue ? (
            <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text)", fontVariantNumeric: "tabular-nums" }}>
              {Math.round(pct)}%
            </span>
          ) : null}
        </div>
      ) : null}
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        style={{
          height: 6,
          width: "100%",
          background: "var(--color-bg-subtle)",
          borderRadius: "var(--radius-full)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${pct}%`,
            background: fill,
            borderRadius: "var(--radius-full)",
            transition: "width var(--duration-base) var(--ease)",
          }}
        />
      </div>
    </div>
  );
}
