/* @ds-bundle: {"format":3,"namespace":"SekaiDesignSystem_2572f3","components":[{"name":"Avatar","sourcePath":"components/core/Avatar.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"ProgressBar","sourcePath":"components/feedback/ProgressBar.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Textarea","sourcePath":"components/forms/Textarea.jsx"},{"name":"DreamCard","sourcePath":"components/product/DreamCard.jsx"}],"sourceHashes":{"components/core/Avatar.jsx":"ebbca818753e","components/core/Badge.jsx":"d3c9a9a9c422","components/core/Button.jsx":"510f9a5e7460","components/core/Card.jsx":"4238c0f99814","components/feedback/ProgressBar.jsx":"a61c2624428b","components/forms/Input.jsx":"be4663ff3b24","components/forms/Select.jsx":"304dc68aa610","components/forms/Textarea.jsx":"a5c266e7c556","components/product/DreamCard.jsx":"0404b2efafbe","ui_kits/dreams/AppShell.jsx":"dce28245d9d6","ui_kits/dreams/Modals.jsx":"0b8e06958d60","ui_kits/dreams/Screens.jsx":"a922d51ef7eb","ui_kits/dreams/data.jsx":"098ffbf051ef"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.SekaiDesignSystem_2572f3 = window.SekaiDesignSystem_2572f3 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const SIZES = {
  sm: 28,
  md: 36,
  lg: 48
};

/**
 * User avatar — image when `src` is set, otherwise initials on a subtle fill.
 */
function Avatar({
  src,
  name = "",
  size = "md",
  className = "",
  style = {},
  ...props
}) {
  const px = typeof size === "number" ? size : SIZES[size] || SIZES.md;
  const initials = name.split(/\s+/).filter(Boolean).slice(0, 2).map(p => p[0]).join("").toUpperCase();
  return /*#__PURE__*/React.createElement("span", _extends({
    className: className,
    style: {
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
      ...style
    }
  }, props), src ? /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: name,
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover"
    }
  }) : initials || "?");
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const TONES = {
  neutral: {
    color: "var(--color-text-muted)",
    background: "var(--color-bg-subtle)",
    border: "var(--color-border)"
  },
  primary: {
    color: "var(--color-primary)",
    background: "var(--color-primary-subtle)",
    border: "transparent"
  },
  success: {
    color: "var(--color-success)",
    background: "var(--color-success-subtle)",
    border: "transparent"
  },
  warning: {
    color: "var(--color-warning)",
    background: "var(--color-warning-subtle)",
    border: "transparent"
  },
  danger: {
    color: "var(--color-danger)",
    background: "var(--color-danger-subtle)",
    border: "transparent"
  }
};

/**
 * Small status/label pill. Optional leading dot for state indicators.
 */
function Badge({
  children,
  tone = "neutral",
  dot = false,
  className = "",
  style = {},
  ...props
}) {
  const t = TONES[tone] || TONES.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    className: className,
    style: {
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
      ...style
    }
  }, props), dot ? /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: "var(--radius-full)",
      background: "currentColor",
      flexShrink: 0
    }
  }) : null, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const VARIANTS = {
  primary: {
    background: "var(--color-primary)",
    color: "#fff",
    borderColor: "transparent"
  },
  secondary: {
    background: "var(--color-surface)",
    color: "var(--color-text)",
    borderColor: "var(--color-border)"
  },
  ghost: {
    background: "transparent",
    color: "var(--color-text-muted)",
    borderColor: "transparent"
  },
  danger: {
    background: "var(--color-surface)",
    color: "var(--color-danger)",
    borderColor: "var(--color-border)"
  }
};
const SIZES = {
  sm: {
    padding: "6px 12px",
    fontSize: "var(--text-sm)"
  },
  md: {
    padding: "8px 16px",
    fontSize: "var(--text-sm)"
  },
  lg: {
    padding: "10px 20px",
    fontSize: "var(--text-md)"
  }
};
const HOVER = {
  primary: "var(--color-primary-hover)",
  secondary: "var(--color-surface-hover)",
  ghost: "var(--color-surface-hover)",
  danger: "var(--color-danger-subtle)"
};

/**
 * Sekai primary action button. Notion-minimal: flat fills, subtle borders,
 * fast color-only feedback. Use at most one `primary` per view section.
 */
function Button({
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
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: className,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    disabled: Tag === "button" ? disabled : undefined,
    "aria-disabled": disabled || undefined,
    style: {
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
      borderColor: variant === "danger" && hover && !disabled ? "var(--color-danger)" : v.borderColor,
      ...style
    }
  }, props), iconLeft ? /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      width: 16,
      height: 16
    }
  }, iconLeft) : null, children, iconRight ? /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      width: 16,
      height: 16
    }
  }, iconRight) : null);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Content grouping container — white surface, subtle border, 8px radius.
 * Optional title/subtitle header and an `interactive` hover state.
 */
function Card({
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
  return /*#__PURE__*/React.createElement("div", _extends({
    className: className,
    onMouseEnter: () => interactive && setHover(true),
    onMouseLeave: () => interactive && setHover(false),
    style: {
      background: "var(--color-surface)",
      border: "1px solid",
      borderColor: hover ? "var(--color-border-strong)" : "var(--color-border)",
      borderRadius: "var(--radius-md)",
      overflow: "hidden",
      cursor: interactive ? "pointer" : "default",
      transition: "border-color var(--duration-base) var(--ease)",
      ...style
    }
  }, props), title || header ? /*#__PURE__*/React.createElement("div", {
    style: {
      padding: `var(--space-4) ${padding}`,
      borderBottom: "1px solid var(--color-border)"
    }
  }, header || /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-normal)"
    }
  }, title), subtitle ? /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 2,
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)"
    }
  }, subtitle) : null)) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding
    }
  }, children), footer ? /*#__PURE__*/React.createElement("div", {
    style: {
      padding: `var(--space-4) ${padding}`,
      borderTop: "1px solid var(--color-border)"
    }
  }, footer) : null);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ProgressBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Thin progress bar for dream completion. Calm — blue fill on a subtle track,
 * optional inline label + percentage.
 */
function ProgressBar({
  value = 0,
  max = 100,
  label,
  showValue = false,
  tone = "primary",
  className = "",
  style = {},
  ...props
}) {
  const pct = Math.max(0, Math.min(100, value / max * 100));
  const fill = {
    primary: "var(--color-primary)",
    success: "var(--color-success)",
    neutral: "var(--color-text-subtle)"
  }[tone] || "var(--color-primary)";
  return /*#__PURE__*/React.createElement("div", _extends({
    className: className,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-2)",
      ...style
    }
  }, props), label || showValue ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      gap: "var(--space-3)"
    }
  }, label ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)"
    }
  }, label) : /*#__PURE__*/React.createElement("span", null), showValue ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text)",
      fontVariantNumeric: "tabular-nums"
    }
  }, Math.round(pct), "%") : null) : null, /*#__PURE__*/React.createElement("div", {
    role: "progressbar",
    "aria-valuenow": value,
    "aria-valuemin": 0,
    "aria-valuemax": max,
    style: {
      height: 6,
      width: "100%",
      background: "var(--color-bg-subtle)",
      borderRadius: "var(--radius-full)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: "100%",
      width: `${pct}%`,
      background: fill,
      borderRadius: "var(--radius-full)",
      transition: "width var(--duration-base) var(--ease)"
    }
  })));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Text input with label, optional error and hint. Subtle border, blue focus ring.
 */
function Input({
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
  const borderColor = error ? "var(--color-danger)" : focus ? "var(--color-primary)" : "var(--color-border)";
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-2)",
      ...style
    }
  }, label ? /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-normal)"
    }
  }, label) : null, /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    type: type,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    "aria-invalid": !!error,
    style: {
      width: "100%",
      padding: "8px 12px",
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-sm)",
      lineHeight: "var(--leading-normal)",
      color: "var(--color-text)",
      background: "var(--color-surface)",
      border: `1px solid ${borderColor}`,
      borderRadius: "var(--radius-sm)",
      boxShadow: focus ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}` : "none",
      outline: "none",
      transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)"
    }
  }, props)), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-danger)"
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)"
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Native select with label and chevron, styled to match Input.
 */
function Select({
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
  const borderColor = error ? "var(--color-danger)" : focus ? "var(--color-primary)" : "var(--color-border)";
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-2)",
      ...style
    }
  }, label ? /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-normal)"
    }
  }, label) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("select", _extends({
    id: inputId,
    value: value,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    "aria-invalid": !!error,
    style: {
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
      boxShadow: focus ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}` : "none",
      outline: "none",
      transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)"
    }
  }, props), options.map(opt => {
    const o = typeof opt === "string" ? {
      value: opt,
      label: opt
    } : opt;
    return /*#__PURE__*/React.createElement("option", {
      key: o.value,
      value: o.value
    }, o.label);
  })), /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "var(--color-text-muted)",
    strokeWidth: "2",
    "aria-hidden": "true",
    style: {
      position: "absolute",
      right: 12,
      top: "50%",
      transform: "translateY(-50%)",
      pointerEvents: "none"
    }
  }, /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M6 9l6 6 6-6"
  }))), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-danger)"
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)"
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Textarea.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Multi-line text input with label, optional hint/error and character counter.
 */
function Textarea({
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
  const borderColor = error ? "var(--color-danger)" : focus ? "var(--color-primary)" : "var(--color-border)";
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-2)",
      ...style
    }
  }, label ? /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-normal)"
    }
  }, label) : null, /*#__PURE__*/React.createElement("textarea", _extends({
    id: inputId,
    rows: rows,
    maxLength: maxLength,
    value: value,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    "aria-invalid": !!error,
    style: {
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
      boxShadow: focus ? `0 0 0 3px ${error ? "var(--color-danger-subtle)" : "var(--color-primary-subtle)"}` : "none",
      outline: "none",
      transition: "border-color var(--duration-base) var(--ease), box-shadow var(--duration-base) var(--ease)"
    }
  }, props)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      gap: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: error ? "var(--color-danger)" : "var(--color-text-muted)"
    }
  }, error || hint || ""), maxLength ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-subtle)",
      flexShrink: 0,
      fontVariantNumeric: "tabular-nums"
    }
  }, value ? value.length : 0, " / ", maxLength) : null));
}
Object.assign(__ds_scope, { Textarea });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Textarea.jsx", error: String((e && e.message) || e) }); }

// components/product/DreamCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const STATUS = {
  draft: {
    tone: "neutral",
    label: "下書き"
  },
  active: {
    tone: "primary",
    label: "進行中"
  },
  done: {
    tone: "success",
    label: "実現済み"
  }
};
function ShareIcon() {
  // X (formerly Twitter) glyph
  return /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "currentColor",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"
  }));
}
function Placeholder() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "var(--color-bg-subtle)",
      color: "var(--color-text-subtle)"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "28",
    height: "28",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("rect", {
    x: "3",
    y: "3",
    width: "18",
    height: "18",
    rx: "2"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "8.5",
    cy: "8.5",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M21 15l-5-5L5 21"
  })));
}

/**
 * Dream card — the core unit of the Sekai Dreams app. Cover image (up to 4,
 * shown as a 1 + 3 mosaic), title, description excerpt, status badge, and a
 * Share-to-X action. Composes Badge.
 */
function DreamCard({
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
  return /*#__PURE__*/React.createElement("div", _extends({
    className: className,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    onClick: onClick,
    style: {
      background: "var(--color-surface)",
      border: "1px solid",
      borderColor: hover ? "var(--color-border-strong)" : "var(--color-border)",
      borderRadius: "var(--radius-md)",
      overflow: "hidden",
      cursor: onClick ? "pointer" : "default",
      display: "flex",
      flexDirection: "column",
      transition: "border-color var(--duration-base) var(--ease)",
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      aspectRatio: "16 / 10",
      background: "var(--color-bg-subtle)"
    }
  }, imgs.length === 0 ? /*#__PURE__*/React.createElement(Placeholder, null) : imgs.length === 1 ? /*#__PURE__*/React.createElement("img", {
    src: imgs[0],
    alt: "",
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  }) : /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "2fr 1fr",
      gridTemplateRows: "1fr 1fr",
      gap: 2,
      height: "100%"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: imgs[0],
    alt: "",
    style: {
      gridRow: "1 / 3",
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  }), imgs.slice(1, 4).map((src, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      position: "relative",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: "",
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  }), i === 2 && extra > 0 ? /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "rgba(25,25,25,0.55)",
      color: "#fff",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)"
    }
  }, "+", extra) : null))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: "var(--space-3)",
      left: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    tone: s.tone,
    dot: true,
    style: {
      background: "rgba(255,255,255,0.92)",
      backdropFilter: "blur(4px)"
    }
  }, s.label))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-4)",
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-2)",
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: "var(--space-2)"
    }
  }, index != null ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-subtle)",
      fontVariantNumeric: "tabular-nums",
      flexShrink: 0
    }
  }, "#", index) : null, /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-tight)",
      margin: 0,
      overflow: "hidden",
      textOverflow: "ellipsis",
      whiteSpace: "nowrap"
    }
  }, title)), description ? /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)",
      lineHeight: "var(--leading-relaxed)",
      margin: 0,
      display: "-webkit-box",
      WebkitLineClamp: 2,
      WebkitBoxOrient: "vertical",
      overflow: "hidden"
    }
  }, description) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "auto",
      paddingTop: "var(--space-3)",
      display: "flex",
      justifyContent: "flex-end"
    }
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: e => {
      e.stopPropagation();
      onShare && onShare();
    },
    style: {
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
      transition: "background-color var(--duration-base) var(--ease), color var(--duration-base) var(--ease)"
    },
    onMouseEnter: e => {
      e.currentTarget.style.background = "var(--color-surface-hover)";
      e.currentTarget.style.color = "var(--color-text)";
    },
    onMouseLeave: e => {
      e.currentTarget.style.background = "transparent";
      e.currentTarget.style.color = "var(--color-text-muted)";
    }
  }, /*#__PURE__*/React.createElement(ShareIcon, null), "\u30B7\u30A7\u30A2"))));
}
Object.assign(__ds_scope, { DreamCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/product/DreamCard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dreams/AppShell.jsx
try { (() => {
// App shell — topbar + sidebar for the Sekai Dreams app.
const {
  useState
} = React;
function Icon({
  path,
  fill = false,
  size = 16,
  stroke = 1.5
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: fill ? "currentColor" : "none",
    stroke: fill ? "none" : "currentColor",
    strokeWidth: stroke,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": "true"
  }, path);
}
const ICONS = {
  home: /*#__PURE__*/React.createElement("path", {
    d: "M2.25 12l8.954-8.955a1.126 1.126 0 011.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75"
  }),
  star: /*#__PURE__*/React.createElement("path", {
    d: "M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
  }),
  check: /*#__PURE__*/React.createElement("path", {
    d: "M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
  }),
  doc: /*#__PURE__*/React.createElement("path", {
    d: "M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
  }),
  settings: /*#__PURE__*/React.createElement("path", {
    d: "M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
  }),
  plus: /*#__PURE__*/React.createElement("path", {
    d: "M12 4.5v15m7.5-7.5h-15"
  }),
  search: /*#__PURE__*/React.createElement("path", {
    d: "M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
  }),
  bell: /*#__PURE__*/React.createElement("path", {
    d: "M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
  }),
  back: /*#__PURE__*/React.createElement("path", {
    d: "M15.75 19.5L8.25 12l7.5-7.5"
  }),
  x: /*#__PURE__*/React.createElement("path", {
    d: "M6 18L18 6M6 6l12 12"
  })
};
function NavItem({
  icon,
  label,
  badge,
  active,
  onClick
}) {
  const [hover, setHover] = useState(false);
  return /*#__PURE__*/React.createElement("a", {
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-2)",
      padding: "6px 8px",
      fontSize: "var(--text-sm)",
      borderRadius: "var(--radius-sm)",
      cursor: "pointer",
      transition: "background-color var(--duration-fast) var(--ease)",
      color: active ? "var(--color-primary)" : "var(--color-text-muted)",
      fontWeight: active ? "var(--weight-medium)" : "var(--weight-normal)",
      background: active ? "var(--color-bg-subtle)" : hover ? "var(--color-surface-hover)" : "transparent"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flexShrink: 0,
      width: 16,
      height: 16,
      display: "inline-flex"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    path: icon,
    stroke: active ? 1.8 : 1.5
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, label), badge != null ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-subtle)",
      fontVariantNumeric: "tabular-nums"
    }
  }, badge) : null);
}
function AppShell({
  active,
  onNav,
  onAdd,
  children
}) {
  const {
    Avatar,
    Button
  } = window.SekaiDesignSystem_2572f3;
  const nav = [{
    key: "dreams",
    icon: ICONS.home,
    label: "すべての夢",
    badge: 9
  }, {
    key: "active",
    icon: ICONS.star,
    label: "進行中",
    badge: 4
  }, {
    key: "done",
    icon: ICONS.check,
    label: "実現済み",
    badge: 3
  }, {
    key: "draft",
    icon: ICONS.doc,
    label: "下書き",
    badge: 2
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: "100vh",
      background: "var(--color-bg)"
    }
  }, /*#__PURE__*/React.createElement("header", {
    style: {
      position: "sticky",
      top: 0,
      zIndex: 20,
      height: "var(--layout-header-height)",
      background: "var(--color-surface)",
      borderBottom: "1px solid var(--color-border)",
      display: "flex",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: "var(--layout-sidebar-width)",
      height: "100%",
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "0 var(--space-6)",
      borderRight: "1px solid var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 20,
      height: 20,
      borderRadius: "var(--radius-full)",
      background: "var(--color-primary)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: "var(--radius-full)",
      background: "#fff"
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-semibold)",
      letterSpacing: "-0.02em",
      color: "var(--color-text)"
    }
  }, "Sekai")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      alignItems: "center",
      padding: "0 var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      width: "100%",
      maxWidth: 360
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: 10,
      top: "50%",
      transform: "translateY(-50%)",
      color: "var(--color-text-subtle)",
      display: "inline-flex"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    path: ICONS.search,
    size: 15
  })), /*#__PURE__*/React.createElement("input", {
    placeholder: "\u5922\u3092\u691C\u7D22",
    style: {
      width: "100%",
      padding: "7px 12px 7px 32px",
      fontSize: "var(--text-sm)",
      fontFamily: "var(--font-sans)",
      color: "var(--color-text)",
      background: "var(--color-bg-subtle)",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-sm)",
      outline: "none"
    }
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      padding: "0 var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement("button", {
    "aria-label": "\u901A\u77E5",
    style: {
      width: 32,
      height: 32,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      borderRadius: "var(--radius-sm)",
      border: "none",
      background: "transparent",
      color: "var(--color-text-muted)",
      cursor: "pointer"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    path: ICONS.bell
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-2)",
      paddingLeft: "var(--space-3)",
      borderLeft: "1px solid var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    name: "Koji Ito",
    size: "sm"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text)"
    }
  }, "Koji")))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      minHeight: "calc(100vh - var(--layout-header-height))"
    }
  }, /*#__PURE__*/React.createElement("aside", {
    style: {
      width: "var(--layout-sidebar-width)",
      flexShrink: 0,
      background: "var(--color-bg-subtle)",
      borderRight: "1px solid var(--color-border)",
      display: "flex",
      flexDirection: "column",
      position: "sticky",
      top: "var(--layout-header-height)",
      height: "calc(100vh - var(--layout-header-height))"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-4)"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "md",
    onClick: onAdd,
    iconLeft: /*#__PURE__*/React.createElement(Icon, {
      path: ICONS.plus
    }),
    style: {
      width: "100%"
    }
  }, "\u5922\u3092\u8FFD\u52A0")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 2,
      padding: "0 var(--space-3)",
      flex: 1
    }
  }, nav.map(n => /*#__PURE__*/React.createElement(NavItem, {
    key: n.key,
    icon: n.icon,
    label: n.label,
    badge: n.badge,
    active: active === n.key,
    onClick: () => onNav(n.key)
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: "var(--space-2) 8px",
      borderTop: "1px solid var(--color-border)"
    }
  }), /*#__PURE__*/React.createElement(NavItem, {
    icon: ICONS.settings,
    label: "\u8A2D\u5B9A",
    active: active === "settings",
    onClick: () => onNav("settings")
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-4) var(--space-5)",
      borderTop: "1px solid var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("a", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)",
      cursor: "pointer"
    }
  }, "\u30B5\u30A4\u30F3\u30A2\u30A6\u30C8"))), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      minWidth: 0,
      overflowY: "auto"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: "var(--layout-content-max-width)",
      margin: "0 auto",
      padding: "var(--space-8)"
    }
  }, children))));
}
Object.assign(window, {
  AppShell,
  Icon,
  ICONS
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dreams/AppShell.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dreams/Modals.jsx
try { (() => {
// Add/edit dream form + share-to-X modal.
const {
  useState: useSt
} = React;
function ImageSlots({
  images,
  onChange
}) {
  const slots = [0, 1, 2, 3];
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
    style: {
      display: "block",
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      marginBottom: "var(--space-2)"
    }
  }, "\u753B\u50CF ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-text-subtle)",
      fontWeight: "var(--weight-normal)"
    }
  }, "\uFF08\u6700\u59274\u679A\uFF09")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: "var(--space-3)"
    }
  }, slots.map(i => {
    const src = images[i];
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      onClick: () => onChange(i),
      style: {
        aspectRatio: "1",
        borderRadius: "var(--radius-sm)",
        overflow: "hidden",
        cursor: "pointer",
        border: src ? "1px solid var(--color-border)" : "1px dashed var(--color-border-strong)",
        background: "var(--color-bg-subtle)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "var(--color-text-subtle)",
        position: "relative"
      }
    }, src ? /*#__PURE__*/React.createElement("img", {
      src: src,
      alt: "",
      style: {
        width: "100%",
        height: "100%",
        objectFit: "cover"
      }
    }) : /*#__PURE__*/React.createElement("svg", {
      width: "20",
      height: "20",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "1.5"
    }, /*#__PURE__*/React.createElement("path", {
      strokeLinecap: "round",
      strokeLinejoin: "round",
      d: "M12 4.5v15m7.5-7.5h-15"
    })));
  })));
}
function DreamForm({
  dream,
  onCancel,
  onSave
}) {
  const {
    Input,
    Textarea,
    Select,
    Button
  } = window.SekaiDesignSystem_2572f3;
  const [title, setTitle] = useSt(dream ? dream.title : "");
  const [desc, setDesc] = useSt(dream ? dream.desc : "");
  const [status, setStatus] = useSt(dream ? dream.status : "active");
  const [images, setImages] = useSt(dream ? dream.images.slice(0, 4) : []);
  const {
    PageHeader
  } = window;
  const toggleImg = i => {
    const next = images.slice();
    if (next[i]) next.splice(i, 1);else next[i] = `https://picsum.photos/seed/new${Date.now() % 1000}-${i}/640/480`;
    setImages(next.filter(Boolean));
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 680,
      margin: "0 auto"
    }
  }, /*#__PURE__*/React.createElement(PageHeader, {
    title: dream ? "夢を編集" : "新しい夢",
    description: "\u4EBA\u751F\u3067\u53F6\u3048\u305F\u3044\u3053\u3068\u3092\u3001\u3072\u3068\u3064\u66F8\u304D\u7559\u3081\u307E\u3057\u3087\u3046\u3002"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement(Input, {
    label: "\u5922\u306E\u30BF\u30A4\u30C8\u30EB",
    placeholder: "\u4F8B: \u30AA\u30FC\u30ED\u30E9\u3092\u898B\u308B",
    value: title,
    onChange: e => setTitle(e.target.value)
  }), /*#__PURE__*/React.createElement(Textarea, {
    label: "\u5922\u306E\u6982\u8981",
    maxLength: 500,
    rows: 5,
    value: desc,
    onChange: e => setDesc(e.target.value),
    placeholder: "\u3053\u306E\u5922\u306B\u3064\u3044\u3066\u3001\u3044\u307E\u306E\u6C17\u6301\u3061\u3092\u66F8\u3044\u3066\u307F\u307E\u3057\u3087\u3046\u3002"
  }), /*#__PURE__*/React.createElement(Select, {
    label: "\u30B9\u30C6\u30FC\u30BF\u30B9",
    value: status,
    onChange: e => setStatus(e.target.value),
    options: [{
      value: "draft",
      label: "下書き"
    }, {
      value: "active",
      label: "進行中"
    }, {
      value: "done",
      label: "実現済み"
    }]
  }), /*#__PURE__*/React.createElement(ImageSlots, {
    images: images,
    onChange: toggleImg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "flex-end",
      gap: "var(--space-3)",
      paddingTop: "var(--space-2)",
      borderTop: "1px solid var(--color-border)",
      marginTop: "var(--space-2)"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    onClick: onCancel
  }, "\u30AD\u30E3\u30F3\u30BB\u30EB"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    onClick: () => onSave({
      title,
      desc,
      status,
      images
    }),
    disabled: !title.trim()
  }, dream ? "保存" : "夢を追加"))));
}
function ShareModal({
  dream,
  onClose
}) {
  const {
    Button,
    Badge
  } = window.SekaiDesignSystem_2572f3;
  const {
    Icon,
    ICONS
  } = window;
  const text = `私の夢 #${dream.n}「${dream.title}」 — Sekai で叶えたい夢を記録中。`;
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: "fixed",
      inset: 0,
      zIndex: 50,
      background: "rgba(25,25,25,0.4)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    onClick: e => e.stopPropagation(),
    style: {
      width: "100%",
      maxWidth: 460,
      background: "var(--color-surface)",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-sm)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "var(--space-5) var(--space-6)",
      borderBottom: "1px solid var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: "var(--text-lg)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)"
    }
  }, "\u5922\u3092\u30B7\u30A7\u30A2"), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    "aria-label": "\u9589\u3058\u308B",
    style: {
      width: 28,
      height: 28,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      border: "none",
      background: "transparent",
      color: "var(--color-text-muted)",
      cursor: "pointer",
      borderRadius: "var(--radius-sm)"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    path: ICONS.x,
    size: 18
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-md)",
      padding: "var(--space-4)",
      marginBottom: "var(--space-5)"
    }
  }, dream.images[0] ? /*#__PURE__*/React.createElement("div", {
    style: {
      aspectRatio: "16/9",
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      marginBottom: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: dream.images[0],
    alt: "",
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  })) : null, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-relaxed)"
    }
  }, text), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-primary)"
    }
  }, "sekai.app/d/", dream.id)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "flex-end",
      gap: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    onClick: onClose
  }, "\u30EA\u30F3\u30AF\u3092\u30B3\u30D4\u30FC"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    onClick: onClose,
    iconLeft: /*#__PURE__*/React.createElement(Icon, {
      path: ICONS.x,
      fill: true,
      size: 14
    })
  }, "X \u306B\u6295\u7A3F")))));
}
Object.assign(window, {
  DreamForm,
  ShareModal
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dreams/Modals.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dreams/Screens.jsx
try { (() => {
// Dream grid (list view), detail, form, and share modal screens.
const {
  useState: useS
} = React;
function PageHeader({
  title,
  description,
  action
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      gap: "var(--space-4)",
      marginBottom: "var(--space-6)"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: "var(--text-xl)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-tight)",
      letterSpacing: "-0.01em"
    }
  }, title), description ? /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 6,
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)"
    }
  }, description) : null), action);
}
function DreamGrid({
  dreams,
  filter,
  onOpen,
  onShare,
  onAdd,
  onFilterChange
}) {
  const {
    DreamCard,
    ProgressBar,
    Button,
    Select
  } = window.SekaiDesignSystem_2572f3;
  const {
    Icon,
    ICONS
  } = window;
  const list = filter === "dreams" ? dreams : dreams.filter(d => d.status === {
    active: "active",
    done: "done",
    draft: "draft"
  }[filter]);
  const doneCount = dreams.filter(d => d.status === "done").length;
  const titles = {
    dreams: "すべての夢",
    active: "進行中",
    done: "実現済み",
    draft: "下書き"
  };
  const descs = {
    dreams: "あなたが人生で叶えたい夢。最大100件まで登録できます。",
    active: "いま動き出している夢。",
    done: "もう叶えた夢。おめでとう。",
    draft: "まだ書きかけの夢。"
  };
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(PageHeader, {
    title: titles[filter],
    description: descs[filter],
    action: /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      size: "md",
      onClick: onAdd,
      iconLeft: /*#__PURE__*/React.createElement(Icon, {
        path: ICONS.plus
      })
    }, "\u5922\u3092\u8FFD\u52A0")
  }), filter === "dreams" ? /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--color-surface)",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-md)",
      padding: "var(--space-5) var(--space-6)",
      marginBottom: "var(--space-6)",
      display: "flex",
      alignItems: "center",
      gap: "var(--space-8)",
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: "var(--space-2)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 32,
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)",
      lineHeight: 1,
      fontVariantNumeric: "tabular-nums"
    }
  }, doneCount), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)"
    }
  }, "/ ", window.TOTAL, " \u5B9F\u73FE")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 200
    }
  }, /*#__PURE__*/React.createElement(ProgressBar, {
    value: doneCount,
    max: window.TOTAL,
    label: "\u4EBA\u751F\u306E\u9032\u6357",
    showValue: true
  }))) : null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: "var(--space-4)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)"
    }
  }, list.length, " \u4EF6\u306E\u5922"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 160
    }
  }, /*#__PURE__*/React.createElement(Select, {
    value: filter,
    onChange: e => onFilterChange(e.target.value),
    options: [{
      value: "dreams",
      label: "すべて表示"
    }, {
      value: "active",
      label: "進行中のみ"
    }, {
      value: "done",
      label: "実現済みのみ"
    }, {
      value: "draft",
      label: "下書きのみ"
    }]
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
      gap: "var(--space-5)"
    }
  }, list.map(d => /*#__PURE__*/React.createElement(DreamCard, {
    key: d.id,
    index: d.n,
    title: d.title,
    description: d.desc,
    images: d.images,
    status: d.status,
    onClick: () => onOpen(d),
    onShare: () => onShare(d)
  }))));
}
function DreamDetail({
  dream,
  onBack,
  onShare,
  onEdit
}) {
  const {
    Badge,
    Button
  } = window.SekaiDesignSystem_2572f3;
  const {
    Icon,
    ICONS
  } = window;
  const [active, setActive] = useS(0);
  const STATUS = {
    draft: ["neutral", "下書き"],
    active: ["primary", "進行中"],
    done: ["success", "実現済み"]
  };
  const s = STATUS[dream.status];
  const imgs = dream.images;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("button", {
    onClick: onBack,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)",
      background: "transparent",
      border: "none",
      cursor: "pointer",
      marginBottom: "var(--space-5)",
      padding: 0
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    path: ICONS.back,
    size: 15
  }), " \u3059\u3079\u3066\u306E\u5922"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: imgs.length ? "1.3fr 1fr" : "1fr",
      gap: "var(--space-8)",
      alignItems: "start"
    }
  }, imgs.length ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      aspectRatio: "4 / 3",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
      border: "1px solid var(--color-border)",
      background: "var(--color-bg-subtle)"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: imgs[active],
    alt: "",
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  })), imgs.length > 1 ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "var(--space-2)",
      marginTop: "var(--space-3)"
    }
  }, imgs.map((src, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    onClick: () => setActive(i),
    style: {
      width: 64,
      height: 64,
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      padding: 0,
      cursor: "pointer",
      border: `2px solid ${i === active ? "var(--color-primary)" : "var(--color-border)"}`,
      background: "none"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: "",
    style: {
      width: "100%",
      height: "100%",
      objectFit: "cover",
      display: "block"
    }
  })))) : null) : null, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      marginBottom: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: s[0],
    dot: true
  }, s[1]), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-subtle)",
      fontVariantNumeric: "tabular-nums"
    }
  }, "\u5922 #", dream.n)), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: "var(--text-xl)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)",
      lineHeight: "var(--leading-tight)",
      marginBottom: "var(--space-4)"
    }
  }, dream.title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "var(--text-md)",
      color: "var(--color-text-muted)",
      lineHeight: "var(--leading-relaxed)",
      marginBottom: "var(--space-6)"
    }
  }, dream.desc || "まだ概要が書かれていません。"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    onClick: () => onShare(dream),
    iconLeft: /*#__PURE__*/React.createElement(Icon, {
      path: ICONS.x,
      fill: true,
      size: 14
    })
  }, "X \u3067\u30B7\u30A7\u30A2"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    onClick: onEdit
  }, "\u7DE8\u96C6")))));
}
Object.assign(window, {
  DreamGrid,
  DreamDetail,
  PageHeader
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dreams/Screens.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dreams/data.jsx
try { (() => {
// Sample data + shared icons for the Sekai Dreams UI kit.
const img = seed => `https://picsum.photos/seed/${seed}/640/480`;
const DREAMS = [{
  id: 1,
  n: 1,
  title: "オーロラを見る",
  status: "active",
  desc: "アイスランドかノルウェーで、冬の夜空を埋めるオーロラを自分の目で見る。写真ではなく、本物の光のカーテンを。",
  images: [img("aurora1"), img("aurora2"), img("aurora3"), img("aurora4")]
}, {
  id: 2,
  n: 2,
  title: "フルマラソンを完走する",
  status: "done",
  desc: "42.195kmを自分の脚で走りきる。タイムは問わない。ゴールテープを切るその瞬間を味わう。",
  images: [img("run1"), img("run2")]
}, {
  id: 3,
  n: 3,
  title: "本を一冊書く",
  status: "draft",
  desc: "いつか自分の言葉で、一冊の本を書き上げたい。テーマはまだ決まっていない。",
  images: []
}, {
  id: 4,
  n: 4,
  title: "京都で桜を見る",
  status: "done",
  desc: "哲学の道を、満開の桜の下で歩く。朝のいちばん静かな時間に。",
  images: [img("sakura1"), img("sakura2"), img("sakura3")]
}, {
  id: 5,
  n: 5,
  title: "ピアノでノクターンを弾く",
  status: "active",
  desc: "ショパンのノクターン第2番を、最後まで通して弾けるようになる。",
  images: [img("piano1")]
}, {
  id: 6,
  n: 6,
  title: "自分のカフェを開く",
  status: "active",
  desc: "小さくていい。好きな珈琲と、静かな音楽と、誰かが長居したくなる席のある店を持つ。",
  images: [img("cafe1"), img("cafe2"), img("cafe3"), img("cafe4"), img("cafe5")]
}, {
  id: 7,
  n: 7,
  title: "両親を旅行に連れて行く",
  status: "draft",
  desc: "元気なうちに、温泉でもいい、ふたりをゆっくりした旅に連れて行きたい。",
  images: []
}, {
  id: 8,
  n: 8,
  title: "星空の下でキャンプ",
  status: "done",
  desc: "街の灯りが届かない場所で、天の川が見えるほどの星空の下、一晩を過ごす。",
  images: [img("camp1"), img("camp2")]
}, {
  id: 9,
  n: 9,
  title: "海外で一年暮らす",
  status: "active",
  desc: "観光ではなく、生活として、ひとつの街に一年腰を据えてみたい。",
  images: [img("city1"), img("city2"), img("city3")]
}];
const TOTAL = 100;
Object.assign(window, {
  DREAMS,
  TOTAL
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dreams/data.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Textarea = __ds_scope.Textarea;

__ds_ns.DreamCard = __ds_scope.DreamCard;

})();
