import type { ReactNode } from "react";

type Props = {
  icon: ReactNode;
  title: string;
  text?: string;
  action?: ReactNode;
};

export default function EmptyState({ icon, title, text, action }: Props) {
  return (
    <div className="empty">
      <span className="empty__icon">{icon}</span>
      <p className="empty__title">{title}</p>
      {text && <p className="empty__text">{text}</p>}
      {action}
    </div>
  );
}
