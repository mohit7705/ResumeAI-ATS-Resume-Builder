import {
  Award,
  Briefcase,
  Folder,
  FileText,
  GraduationCap,
  LayoutDashboard,
  Mail,
  AlignLeft,
  Trophy,
  User,
  Wrench,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { Page } from "../context/AppContext";

export type NavItem = {
  value: Page;
  title: string;
  description: string;
  icon: LucideIcon;
};

export type NavGroup = {
  title: string;
  items: NavItem[];
};

export const NAV_GROUPS: NavGroup[] = [
  {
    title: "Overview",
    items: [
      {
        value: "dashboard",
        title: "Dashboard",
        description: "Build an ATS-friendly resume with AI",
        icon: LayoutDashboard,
      },
    ],
  },
  {
    title: "Your details",
    items: [
      {
        value: "profile",
        title: "Profile",
        description: "Your name and professional title",
        icon: User,
      },
      {
        value: "contact",
        title: "Contact",
        description: "How recruiters can reach you",
        icon: Mail,
      },
      {
        value: "summary",
        title: "Summary",
        description: "A short introduction for the top of your resume",
        icon: AlignLeft,
      },
      {
        value: "education",
        title: "Education",
        description: "Degrees, colleges and results",
        icon: GraduationCap,
      },
      {
        value: "experience",
        title: "Experience",
        description: "Internships and jobs you have done",
        icon: Briefcase,
      },
      {
        value: "skills",
        title: "Technical skills",
        description: "Choose which skills appear on your resume",
        icon: Wrench,
      },
      {
        value: "projects",
        title: "Projects",
        description: "Work you have built and shipped",
        icon: Folder,
      },
      {
        value: "certifications",
        title: "Certifications",
        description: "Courses and credentials you have earned",
        icon: Award,
      },
      {
        value: "achievements",
        title: "Achievements",
        description: "Awards and milestones worth mentioning",
        icon: Trophy,
      },
    ],
  },
  {
    title: "Output",
    items: [
      {
        value: "resume",
        title: "Resume generator",
        description: "Create an ATS-friendly resume for a specific job",
        icon: FileText,
      },
    ],
  },
];

export const NAV_ITEMS: NavItem[] = NAV_GROUPS.flatMap((group) => group.items);

export function findNav(page: Page) {
  const group = NAV_GROUPS.find((g) => g.items.some((i) => i.value === page));
  const item = NAV_ITEMS.find((i) => i.value === page);
  return { group, item };
}
