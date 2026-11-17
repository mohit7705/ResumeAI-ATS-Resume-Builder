import { useEffect, useState } from "react";
import { FileText } from "lucide-react";

import { useApp } from "../context/AppContext";
import { getProfile } from "../services/personal";
import { initials } from "../utils/format";
import { NAV_GROUPS } from "./nav";

type Props = {
  open: boolean;
  onNavigate: () => void;
};

export default function Sidebar({ open, onNavigate }: Props) {
  const { page, setPage } = useApp();
  const [profile, setProfile] = useState<any>(null);

  // Re-read the profile when the page changes so the name stays fresh after saving.
  useEffect(() => {
    let cancelled = false;

    getProfile()
      .then((data) => {
        if (!cancelled) setProfile(data);
      })
      .catch(() => {
        /* the sidebar works without it */
      });

    return () => {
      cancelled = true;
    };
  }, [page]);

  const fullName = [profile?.first_name, profile?.last_name]
    .filter(Boolean)
    .join(" ");

  return (
    <aside className="sidebar" data-open={open} aria-label="Main navigation">
      <div className="sidebar__brand">
        <span className="brand-mark">
          <FileText size={20} />
        </span>

        <div>
          <div className="brand-name">ResumeAI</div>
          <div className="brand-tag">ATS resume builder</div>
        </div>
      </div>

      <nav className="sidebar__nav">
        {NAV_GROUPS.map((group) => (
          <div className="nav-group" key={group.title}>
            <div className="nav-group__title">{group.title}</div>

            {group.items.map((item) => {
              const Icon = item.icon;

              return (
                <button
                  key={item.value}
                  type="button"
                  className="nav-item"
                  aria-current={page === item.value ? "page" : undefined}
                  onClick={() => {
                    setPage(item.value);
                    onNavigate();
                  }}
                >
                  <Icon size={18} />
                  {item.title}
                </button>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="sidebar__foot">
        <div className="user-chip">
          <span className="avatar">
            {initials(profile?.first_name, profile?.last_name)}
          </span>

          <div>
            <div className="user-chip__name">
              {fullName || "Your profile"}
            </div>
            <div className="user-chip__meta">
              {profile?.professional_title || "Add your title in Profile"}
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
