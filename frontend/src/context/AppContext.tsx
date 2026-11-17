import { createContext, useContext, useState } from "react";

export type Page =
  | "dashboard"
  | "profile"
  | "contact"
  | "summary"
  | "education"
  | "experience"
  | "skills"
  | "projects"
  | "certifications"
  | "achievements"
  | "resume";

interface AppContextType {
  page: Page;
  setPage: React.Dispatch<React.SetStateAction<Page>>;
}

const AppContext = createContext<AppContextType>(null!);

export function AppProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [page, setPage] = useState<Page>("dashboard");

  return (
    <AppContext.Provider
      value={{
        page,
        setPage,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
