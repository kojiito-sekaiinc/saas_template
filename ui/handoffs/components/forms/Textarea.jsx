import React from "react";

/**
 * Multi-line text input with label, optional hint/error and character counter.
 */
export function Textarea({
  label,
  hint,
  error,
  id,
  rows = 4,
  maxLength,
  value,
  className = "",
  style = {},
  ...props
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || (label ? `ta-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
  const borderColor = error
    ? "var(--color-danger)"
    : focus
    ? "var(--color-primary)"
    : "var(--color-border)";

  return (
    <div className={className} style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)", ...style }}>
      {label ? (
        <label
          htmlFor={inputId}
          style={{
            fontSize: "var(--text-sm)",
            fontWeight: "var(--weight-medium)",
            color: "var(--color-text)",
            lineHeight: "var(--leading-normal)",
          }}
        >
          {label}
        </label>
      ) : null}
      <textarea
        id={inputId}
        rows={rows}
        maxLength={maxLength}
        value={value}
        onFocus={() => setFocus(true)}
        onBlur={() => setFocus(false)}
        aria-invalid={!!error}
        style={{
          width: "100%",
          padding: "8px 12px",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-sm)",
          lineHeight: "var(--leading-relaxed)",
          color: "var(--color-text)",
          background: "var(--color-surface)",
          border: `1px solid ${borderColor}`,
          borderRadius: "var(--radius-sm)",
          resize: "vertical",
          boxShadow: focus
            ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}`
            : "none",
          outline: "none",
          transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)",
        }}
        {...props}
      />
      <div style={{ display: "flex", justifyContent: "space-between", gap: "var(--space-3)" }}>
        <span style={{ fontSize: "var(--text-xs)", color: error ? "var(--color-danger)" : "var(--color-text-muted)" }}>
          {error || hint || ""}
        </span>
        {maxLength ? (
          <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-subtle)", flexShrink: 0, fontVariantNumeric: "tabular-nums" }}>
            {(value ? value.length : 0)} / {maxLength}
          </span>
        ) : null}
      </div>
    </div>
  );
}
