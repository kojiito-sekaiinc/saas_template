import React from "react";

const VARIANTS = {
  primary: {
    background: "var(--color-primary)",
    color: "#fff",
    borderColor: "transparent",
  },
  secondary: {
    background: "var(--color-surface)",
    color: "var(--color-text)",
    borderColor: "var(--color-border)",
  },
  ghost: {
    background: "transparent",
    color: "var(--color-text-muted)",
    borderColor: "transparent",
  },
  danger: {
    background: "var(--color-surface)",
    color: "var(--color-danger)",
    borderColor: "var(--color-border)",
  },
};

const SIZES = {
  sm: { padding: "6px 12px", fontSize: "var(--text-sm)" },
  md: { padding: "8px 16px", fontSize: "var(--text-sm)" },
  lg: { padding: "10px 20px", fontSize: "var(--text-md)" },
};

const HOVER = {
  primary: "var(--color-primary-hover)",
  secondary: "var(--color-surface-hover)",
  ghost: "var(--color-surface-hover)",
  danger: "var(--color-danger-subtle)",
};

/**
 * Sekai primary action button. Notion-minimal: flat fills, subtle borders,
 * fast color-only feedback. Use at most one `primary` per view section.
 */
export function Button({
  children,
  variant = "primary",
  size = "md",
  disabled = false,
  iconLeft = null,
  iconRight = null,
  as = "button",
  className = "",
  style = {},
  ...props
}) {
  const [hover, setHover] = React.useState(false);
  const v = VARIANTS[variant] || VARIANTS.primary;
  const s = SIZES[size] || SIZES.md;
  const Tag = as;

  return (
    <Tag
      className={className}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      disabled={Tag === "button" ? disabled : undefined}
      aria-disabled={disabled || undefined}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "var(--space-2)",
        ...s,
        fontFamily: "var(--font-sans)",
        fontWeight: "var(--weight-medium)",
        lineHeight: "var(--leading-normal)",
        borderRadius: "var(--radius-md)",
        border: "1px solid",
        whiteSpace: "nowrap",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.5 : 1,
        transition: "background-color var(--duration-base) var(--ease), border-color var(--duration-base) var(--ease)",
        ...v,
        background: disabled || !hover ? v.background : HOVER[variant],
        borderColor:
          variant === "danger" && hover && !disabled
            ? "var(--color-danger)"
            : v.borderColor,
        ...style,
      }}
      {...props}
    >
      {iconLeft ? <span style={{ display: "inline-flex", width: 16, height: 16 }}>{iconLeft}</span> : null}
      {children}
      {iconRight ? <span style={{ display: "inline-flex", width: 16, height: 16 }}>{iconRight}</span> : null}
    </Tag>
  );
}
