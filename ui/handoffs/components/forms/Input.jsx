import React from "react";

/**
 * Text input with label, optional error and hint. Subtle border, blue focus ring.
 */
export function Input({
  label,
  hint,
  error,
  id,
  type = "text",
  className = "",
  style = {},
  ...props
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || (label ? `in-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
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
      <input
        id={inputId}
        type={type}
        onFocus={() => setFocus(true)}
        onBlur={() => setFocus(false)}
        aria-invalid={!!error}
        style={{
          width: "100%",
          padding: "8px 12px",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-sm)",
          lineHeight: "var(--leading-normal)",
          color: "var(--color-text)",
          background: "var(--color-surface)",
          border: `1px solid ${borderColor}`,
          borderRadius: "var(--radius-sm)",
          boxShadow: focus
            ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}`
            : "none",
          outline: "none",
          transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)",
        }}
        {...props}
      />
      {error ? (
        <span style={{ fontSize: "var(--text-xs)", color: "var(--color-danger)" }}>{error}</span>
      ) : hint ? (
        <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-muted)" }}>{hint}</span>
      ) : null}
    </div>
  );
}
