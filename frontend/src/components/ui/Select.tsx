import type { SelectHTMLAttributes } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "../../utils/cn";

type Props = SelectHTMLAttributes<HTMLSelectElement>;

export default function Select({ className, children, ...rest }: Props) {
  return (
    <div className="select-wrap">
      <select {...rest} className={cn("select", className)}>
        {children}
      </select>
      <ChevronDown size={16} aria-hidden="true" />
    </div>
  );
}
