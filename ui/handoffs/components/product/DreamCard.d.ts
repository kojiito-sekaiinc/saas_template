import { CSSProperties } from "react";

/**
 * Dream card — the core unit of the Sekai Dreams app. Renders a cover mosaic
 * (up to 4 images as a 1 + 3 layout), title, 2-line description excerpt,
 * status badge, and a Share-to-X action. Composes Badge.
 *
 * @startingPoint section="Product" subtitle="Dream card with cover + status" viewport="360x360"
 */
export interface DreamCardProps {
  title: string;
  description?: string;
  /** Up to 4 image URLs are shown; extras collapse into a "+N" overlay. */
  images?: string[];
  status?: "draft" | "active" | "done";
  /** Optional 1-based position number shown as "#index". */
  index?: number;
  onShare?: () => void;
  onClick?: () => void;
  className?: string;
  style?: CSSProperties;
  [key: string]: any;
}

export function DreamCard(props: DreamCardProps): JSX.Element;
