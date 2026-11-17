import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import Button from "./Button";

type Props = {
  onConfirm: () => void;
  label?: string;
};

/** Two-step delete: first click arms it, second click confirms. */
export default function DeleteButton({ onConfirm, label = "Delete" }: Props) {
  const [armed, setArmed] = useState(false);

  useEffect(() => {
    if (!armed) return;
    const timer = window.setTimeout(() => setArmed(false), 3000);
    return () => window.clearTimeout(timer);
  }, [armed]);

  return (
    <Button
      variant="danger"
      size="sm"
      data-confirm={armed}
      aria-label={armed ? `Confirm ${label.toLowerCase()}` : label}
      icon={<Trash2 size={14} />}
      onClick={() => {
        if (armed) {
          setArmed(false);
          onConfirm();
        } else {
          setArmed(true);
        }
      }}
    >
      {armed ? "Confirm?" : label}
    </Button>
  );
}
