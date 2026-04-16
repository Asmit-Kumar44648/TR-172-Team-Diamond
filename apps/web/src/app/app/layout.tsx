"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  Box, 
  Database, 
  Key, 
  Settings, 
  CreditCard, 
  FileText, 
  PlusCircle,
  BarChart2
} from "lucide-react";

const NAV_LINKS = [
  { name: "New analysis", href: "/app/upload", icon: PlusCircle },
  { name: "Analyses", href: "/app/analyses", icon: BarChart2 },
  { separator: true },
  { name: "API keys", href: "/app/settings?tab=keys", icon: Key },
  { name: "Settings", href: "/app/settings", icon: Settings },
  { name: "Billing", href: "/app/settings?tab=billing", icon: CreditCard },
  { name: "Docs", href: "/app/docs", icon: FileText },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-screen bg-background text-zinc-300">
      {/* Sidebar 220px */}
      <aside className="w-[220px] fixed inset-y-0 border-r border-border bg-background flex flex-col p-4">
        <div className="mb-8">
          <div className="text-sm font-semibold text-zinc-100">GRASP</div>
          <div className="text-xs text-zinc-500">Autonomous Corp</div>
        </div>

        <nav className="flex-1 space-y-1">
          {NAV_LINKS.map((link, idx) => {
            if (link.separator) {
              return <div key={`sep-${idx}`} className="h-px bg-border my-4" />;
            }

            const Icon = link.icon!;
            const active = pathname === link.href || (link.href !== "/app/upload" && pathname?.startsWith(link.href!));

            return (
              <Link
                key={link.name}
                href={link.href!}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors duration-200",
                  active 
                    ? "bg-surfaceElevated text-zinc-100" 
                    : "text-zinc-500 hover:text-zinc-200 hover:bg-surfaceElevated/50"
                )}
              >
                <Icon size={16} />
                {link.name}
              </Link>
            );
          })}
        </nav>

        {/* Quota Meter */}
        <div className="mt-auto pt-6 border-t border-border">
          <div className="flex justify-between text-xs mb-2">
            <span className="text-zinc-500">2 / 5 today</span>
            <Link href="/app/settings?tab=billing" className="text-accent hover:underline">Upgrade</Link>
          </div>
          <div className="h-1.5 w-full bg-zinc-800 rounded-full overflow-hidden">
            <div className="h-full bg-accent w-[40%]" />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="pl-[220px] flex-1">
        {children}
      </main>
    </div>
  );
}
