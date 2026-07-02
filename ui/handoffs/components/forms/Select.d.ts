import { CSSProperties } from "react";

export interface SelectOption {
  value: string;
  label: string;
}

/**
 * Native select styled to match Input — label, chevron, blue focus ring.
 * `options` accepts plain strings or {value,label} objects.
 */
export interface SelectProps {
  label?: string;
  hint?: string;
  error?: string;
  id?: string;
  options?: Array<string | SelectOption>;
  value?: string;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Select(props: SelectProps): JSX.Element;
