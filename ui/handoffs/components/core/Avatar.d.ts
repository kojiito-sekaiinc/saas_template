import { CSSProperties } from "react";

/**
 * User avatar — shows `src` image, or initials derived from `name`.
 */
export interface AvatarProps {
  src?: string;
  name?: string;
  size?: "sm" | "md" | "lg" | number;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function Avatar(props: AvatarProps): JSX.Element;
