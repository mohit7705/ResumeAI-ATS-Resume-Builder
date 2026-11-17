import type { TextareaHTMLAttributes } from "react";
import { cn } from "../../utils/cn";

type Props = TextareaHTMLAttributes<HTMLTextAreaElement>;

export default function TextArea({ className, ...rest }: Props) {
  return <textarea {...rest} className={cn("textarea", className)} />;
}
