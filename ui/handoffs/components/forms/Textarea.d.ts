import { CSSProperties } from "react";

/**
 * Multi-line text input with label, hint/error and an optional character
 * counter (shown when `maxLength` is set).
 */
export interface TextareaProps {
  label?: string;
  hint?: string;
  error?: string;
  id?: string;
  rows?: number;
  maxLength?: number;
  value?: string;
  placeholder?: string;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Textarea(props: TextareaProps): JSX.Element;
