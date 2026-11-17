import type { ReactNode } from "react";
import { cn } from "../../utils/cn";

type Props = {
  value: number;
  size?: number;
  stroke?: number;
  tone?: "accent" | "ok" | "warn";
  small?: boolean;
  children?: ReactNode;
};

export default function Ring({
  value,
  size = 132,
  stroke = 10,
  tone = "accent",
  small,
  children,
}: Props) {
  const safe = Number.isFinite(value) ? Math.min(100, Math.max(0, value)) : 0;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;

  return (
    <div
      className={cn("ring", small && "ring--sm")}
      data-tone={tone}
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} aria-hidden="true">
        <circle
          className="ring__track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={stroke}
        />
        <circle
          className="ring__value"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - safe / 100)}
        />
      </svg>

      <div className="ring__center">
        {children ?? <span className="ring__number">{Math.round(safe)}%</span>}
      </div>
    </div>
  );
}
