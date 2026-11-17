import { Download, Eye, Sparkles } from "lucide-react";

import { useApp } from "../../../context/AppContext";

type Props = {
  title: string;
  description: string;
  action: string;
};

export default function QuickAction({ title, description, action }: Props) {
  const { setPage } = useApp();

  function handleClick() {

    if (action === "generate") {
      // Navigate inside the app (a full page load to /resume would reset it).
      setPage("resume");
    }

    if (action === "preview") {
      window.open(
        "/generated/html/resume.html",
        "_blank"
      );
    }

    if (action === "download") {
      window.open(
        "/generated/pdf/resume.pdf",
        "_blank"
      );
    }

  }

  const Icon =
    action === "generate" ? Sparkles : action === "preview" ? Eye : Download;

  return (
    <button type="button" className="action" onClick={handleClick}>
      <span className="action__icon">
        <Icon size={18} />
      </span>

      <span>
        <span className="action__title">{title}</span>
        <span className="action__text">{description}</span>
      </span>
    </button>
  );
}
