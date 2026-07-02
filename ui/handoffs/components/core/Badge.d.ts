import { ReactNode, CSSProperties } from "react";

/**
 * Small status/label pill. `tone` maps to the semantic color set;
 * `dot` adds a leading state indicator dot.
 */
export interface BadgeProps {
  children: ReactNode;
  tone?: "neutral" | "primary" | "success" | "warning" | "danger";
  dot?: boolean;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Badge(props: BadgeProps): JSX.Element;
