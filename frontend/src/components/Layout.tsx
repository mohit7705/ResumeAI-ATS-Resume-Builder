import { useEffect, useState } from "react";

import { useApp } from "../context/AppContext";
import Sidebar from "./Sidebar";
import Header from "./Header";
import Content from "./Content";

export default function Layout() {
  const { page } = useApp();
  const [menuOpen, setMenuOpen] = useState(false);

  // Close the mobile drawer on Escape.
  useEffect(() => {
    if (!menuOpen) return;

    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setMenuOpen(false);
    };

    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [menuOpen]);

  // Start every page at the top.
  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [page]);

  return (
    <div className="app">
      <Sidebar open={menuOpen} onNavigate={() => setMenuOpen(false)} />

      <div
        className="scrim"
        data-open={menuOpen}
        onClick={() => setMenuOpen(false)}
        aria-hidden="true"
      />

      <div className="main">
        <Header onMenu={() => setMenuOpen(true)} />

        <main className="content">
          <Content />
        </main>
      </div>
    </div>
  );
}
