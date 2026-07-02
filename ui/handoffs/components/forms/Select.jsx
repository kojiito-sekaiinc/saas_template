import React from "react";

/**
 * Native select with label and chevron, styled to match Input.
 */
export function Select({
  label,
  hint,
  error,
  id,
  options = [],
  value,
  className = "",
  style = {},
  ...props
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || (label ? `sel-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
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
      <div style={{ position: "relative" }}>
        <select
          id={inputId}
          value={value}
          onFocus={() => setFocus(true)}
          onBlur={() => setFocus(false)}
          aria-invalid={!!error}
          style={{
            width: "100%",
            padding: "8px 36px 8px 12px",
            fontFamily: "var(--font-sans)",
            fontSize: "var(--text-sm)",
            lineHeight: "var(--leading-normal)",
            color: "var(--color-text)",
            background: "var(--color-surface)",
            border: `1px solid ${borderColor}`,
            borderRadius: "var(--radius-sm)",
            appearance: "none",
            cursor: "pointer",
            boxShadow: focus
              ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}`
              : "none",
            outline: "none",
            transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)",
          }}
          {...props}
        >
          {options.map((opt) => {
            const o = typeof opt === "string" ? { value: opt, label: opt } : opt;
            return (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            );
          })}
        </select>
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--color-text-muted)"
          strokeWidth="2"
          aria-hidden="true"
          style={{ position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 9l6 6 6-6" />
        </svg>
      </div>
      {error ? (
        <span style={{ fontSize: "var(--text-xs)", color: "var(--color-danger)" }}>{error}</span>
      ) : hint ? (
        <span style={{ fontSize: "var(--text-xs)", color: "var(--color-text-muted)" }}>{hint}</span>
      ) : null}
    </div>
  );
}
