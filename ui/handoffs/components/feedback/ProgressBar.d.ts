import { CSSProperties } from "react";

/**
 * Thin progress bar for dream completion — blue fill on a subtle track,
 * with optional label and percentage readout.
 */
export interface ProgressBarProps {
  value?: number;
  max?: number;
  label?: string;
  showValue?: boolean;
  tone?: "primary" | "success" | "neutral";
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function ProgressBar(props: ProgressBarProps): JSX.Element;
