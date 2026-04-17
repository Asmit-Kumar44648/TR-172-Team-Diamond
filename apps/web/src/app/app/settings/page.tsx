"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Key, User, Copy, Trash2, Plus } from "lucide-react";

function SettingsContent() {
  const searchParams = useSearchParams();
  const activeTab = searchParams.get("tab") || "general";

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-sm font-medium text-zinc-200 tracking-wide uppercase mb-1">Organization Settings</h1>
        <p className="text-xs text-zinc-500 uppercase tracking-tight">Manage your workspace and credentials</p>
      </div>

      <div className="flex gap-12">
        <aside className="w-48 flex-shrink-0 space-y-1">
          {[
            { id: "general", label: "General", icon: User },
            { id: "keys", label: "API Keys", icon: Key },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => window.history.pushState(null, "", `?tab=${t.id}`)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                activeTab === t.id ? "bg-surface text-zinc-100" : "text-zinc-500 hover:text-zinc-300"
              )}
            >
              <t.icon size={14} />
              {t.label}
            </button>
          ))}
        </aside>

        <main className="flex-1 space-y-6">
          {activeTab === "keys" && (
            <div className="space-y-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>API Credentials</CardTitle>
                    <CardDescription>Authentication for the Python SDK and CLI</CardDescription>
                  </div>
                  <Button size="sm" className="gap-2">
                    <Plus size={14} /> Create Key
                  </Button>
                </CardHeader>
                <CardContent>
                  <table className="w-full text-left text-xs">
                    <thead className="text-zinc-500 border-b border-border pb-2">
                      <tr>
                        <th className="pb-2 font-medium">Name</th>
                        <th className="pb-2 font-medium">Prefix</th>
                        <th className="pb-2 font-medium">Last used</th>
                        <th className="pb-2 font-medium text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border/50">
                      <tr>
                        <td className="py-4 text-zinc-200">Main Production</td>
                        <td className="py-4 font-mono text-zinc-500">grsp_live_abc123...</td>
                        <td className="py-4 text-zinc-500">2 hours ago</td>
                        <td className="py-4 text-right">
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-zinc-500"><Copy size={14}/></Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-red-500/50 hover:text-red-500"><Trash2 size={14}/></Button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === "general" && (
            <Card>
              <CardHeader>
                <CardTitle>Workspace Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-2">
                  <label className="text-[10px] text-zinc-500 uppercase font-bold">Organization Name</label>
                  <input className="bg-surface border border-border rounded p-2 text-sm outline-none focus:ring-1 focus:ring-accent" defaultValue="Autonomous Corp" />
                </div>
                <div className="grid gap-2">
                  <label className="text-[10px] text-zinc-500 uppercase font-bold">Contact Email</label>
                  <input className="bg-surface border border-border rounded p-2 text-sm outline-none focus:ring-1 focus:ring-accent" defaultValue="ops@autonomous.ai" />
                </div>
                <Button variant="outline" className="w-fit">Save Changes</Button>
              </CardContent>
            </Card>
          )}
        </main>
      </div>
    </div>
  );
}

export default function SettingsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-zinc-500 text-sm">Loading settings...</div>}>
      <SettingsContent />
    </Suspense>
  );
}
