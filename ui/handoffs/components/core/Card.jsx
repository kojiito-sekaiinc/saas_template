import React from "react";

/**
 * Content grouping container — white surface, subtle border, 8px radius.
 * Optional title/subtitle header and an `interactive` hover state.
 */
export function Card({
  children,
  title,
  subtitle,
  header,
  footer,
  interactive = false,
  padding = "var(--space-6)",
  className = "",
  style = {},
  ...props
}) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      className={className}
      onMouseEnter={() => interactive && setHover(true)}
      onMouseLeave={() => interactive && setHover(false)}
      style={{
        background: "var(--color-surface)",
        border: "1px solid",
        borderColor: hover ? "var(--color-border-strong)" : "var(--color-border)",
        borderRadius: "var(--radius-md)",
        overflow: "hidden",
        cursor: interactive ? "pointer" : "default",
        transition: "border-color var(--duration-base) var(--ease)",
        ...style,
      }}
      {...props}
    >
      {title || header ? (
        <div
          style={{
            padding: `var(--space-4) ${padding}`,
            borderBottom: "1px solid var(--color-border)",
          }}
        >
          {header || (
            <>
              <h3
                style={{
                  fontSize: "var(--text-sm)",
                  fontWeight: "var(--weight-medium)",
                  color: "var(--color-text)",
                  lineHeight: "var(--leading-normal)",
                }}
              >
                {title}
              </h3>
              {subtitle ? (
                <p style={{ marginTop: 2, fontSize: "var(--text-xs)", color: "var(--color-text-muted)" }}>
                  {subtitle}
                </p>
              ) : null}
            </>
          )}
        </div>
      ) : null}
      <div style={{ padding }}>{children}</div>
      {footer ? (
        <div style={{ padding: `var(--space-4) ${padding}`, borderTop: "1px solid var(--color-border)" }}>
          {footer}
        </div>
      ) : null}
    </div>
  );
}
