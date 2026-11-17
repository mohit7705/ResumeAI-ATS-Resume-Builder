import { cloneElement, useId } from "react";
import type { ReactElement, ReactNode } from "react";
import { cn } from "../../utils/cn";

type Props = {
  label: string;
  required?: boolean;
  hint?: string;
  wide?: boolean;
  children: ReactElement<{ id?: string }>;
  extra?: ReactNode;
};

/** Label + control + optional hint, wired together for accessibility. */
export default function Field({
  label,
  required,
  hint,
  wide,
  children,
  extra,
}: Props) {
  const id = useId();

  return (
    <div className={cn("field", wide && "span-2")}>
      <label className="label" htmlFor={id}>
        {label}
        {required && (
          <span className="label__req" aria-hidden="true">
            *
          </span>
        )}
      </label>

      {cloneElement(children, { id })}

      {hint && <span className="hint">{hint}</span>}
      {extra}
    </div>
  );
}
