import { ReactNode, CSSProperties } from "react";

/**
 * Primary action button for the Sekai system. Flat fills, subtle borders,
 * fast color-only feedback. Use at most one `primary` per view section.
 *
 * @startingPoint section="Core" subtitle="Button variants & sizes" viewport="700x140"
 */
export interface ButtonProps {
  children: ReactNode;
  /** Visual style. @default "primary" */
  variant?: "primary" | "secondary" | "ghost" | "danger";
  /** @default "md" */
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
  /** Render as a different element, e.g. "a" for links. @default "button" */
  as?: "button" | "a";
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Button(props: ButtonProps): JSX.Element;
