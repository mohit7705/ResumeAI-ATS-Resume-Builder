import { Menu, Moon, Sparkles, Sun } from "lucide-react";

import { useApp } from "../context/AppContext";
import { useTheme } from "../context/ThemeContext";
import Button from "./ui/Button";
import { findNav } from "./nav";

type Props = {
  onMenu: () => void;
};

export default function Header({ onMenu }: Props) {
  const { page, setPage } = useApp();
  const { theme, toggleTheme } = useTheme();
  const { group, item } = findNav(page);

  const isDark = theme === "dark";

  return (
    <header className="topbar">
      <Button
        className="menu-button"
        variant="ghost"
        iconOnly
        aria-label="Open navigation"
        icon={<Menu size={20} />}
        onClick={onMenu}
      />

      <div className="topbar__crumbs">
        <span className="hide-sm">{group?.title}</span>
        <span className="hide-sm" aria-hidden="true">
          /
        </span>
        <strong>{item?.title}</strong>
      </div>

      <div className="topbar__spacer" />

      {page !== "resume" && page !== "dashboard" && (
        <Button
          size="sm"
          className="hide-sm"
          icon={<Sparkles size={14} />}
          onClick={() => setPage("resume")}
        >
          Generate resume
        </Button>
      )}

      <Button
        variant="secondary"
        iconOnly
        aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
        title={isDark ? "Switch to light theme" : "Switch to dark theme"}
        icon={isDark ? <Sun size={18} /> : <Moon size={18} />}
        onClick={toggleTheme}
      />
    </header>
  );
}
