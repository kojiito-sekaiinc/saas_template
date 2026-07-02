import { CSSProperties } from "react";

/**
 * Text input with label, optional hint and error state.
 * Subtle border, blue focus ring; red ring + message when `error` is set.
 */
export interface InputProps {
  label?: string;
  hint?: string;
  error?: string;
  id?: string;
  type?: string;
  placeholder?: string;
  value?: string;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Input(props: InputProps): JSX.Element;
