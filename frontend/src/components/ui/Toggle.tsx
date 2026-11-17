import type { InputHTMLAttributes, ReactNode } from "react";

type Props = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  children?: ReactNode;
};

export default function Toggle({ children, ...rest }: Props) {
  return (
    <label className="toggle">
      <input {...rest} type="checkbox" />
      <span className="toggle__track" aria-hidden="true" />
      {children && <span>{children}</span>}
    </label>
  );
}
