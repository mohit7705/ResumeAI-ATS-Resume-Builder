import type { LucideIcon } from "lucide-react";

type Props = {
  title: string;
  value: string | number;
  icon: LucideIcon;
  onClick?: () => void;
};

export default function StatCard({ title, value, icon: Icon, onClick }: Props) {
  return (
    <button type="button" className="stat" onClick={onClick}>
      <span className="stat__icon">
        <Icon size={22} />
      </span>

      <span>
        <span className="stat__value">{value}</span>
        <span className="stat__label">{title}</span>
      </span>
    </button>
  );
}
