import { ReactNode, CSSProperties } from "react";

/**
 * Content grouping card — white surface, subtle border, 8px radius.
 * Optional header (title + subtitle, or custom `header`) and `footer`.
 * Set `interactive` for a hover border state on clickable cards.
 */
export interface CardProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  header?: ReactNode;
  footer?: ReactNode;
  interactive?: boolean;
  /** Inner padding (CSS value). @default "var(--space-6)" */
  padding?: string;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Card(props: CardProps): JSX.Element;
