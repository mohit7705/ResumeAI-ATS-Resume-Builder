import type { ReactNode } from "react";
import { cn } from "../../utils/cn";

type Props = {
  children: ReactNode;
  tone?: "neutral" | "accent" | "ok" | "warn";
  small?: boolean;
};

export default function Chip({ children, tone = "neutral", small }: Props) {
  return (
    <span
      className={cn(
        "chip",
        tone !== "neutral" && `chip--${tone}`,
        small && "chip--sm"
      )}
    >
      {children}
    </span>
  );
}
