"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PlusCircle, Search } from "lucide-react";

const DEMO_ANALYSES = [
  { id: "job-001", date: "2026-04-16", scene: "bin_picking_01.npz", objects: 5, colFree: "80%", safeAvg: "0.824", status: "COMPLETE" },
  { id: "job-002", date: "2026-04-15", scene: "random_clutter.npz", objects: 12, colFree: "42%", safeAvg: "0.451", status: "COMPLETE" },
  { id: "job-003", date: "2026-04-14", scene: "clear_table.npy", objects: 2, colFree: "100%", safeAvg: "0.912", status: "COMPLETE" },
];

export default function AnalysesPage() {
  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-end border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-sm font-medium text-zinc-200 tracking-wide uppercase mb-1">Analyses History</h1>
          <p className="text-xs text-zinc-500 uppercase tracking-tight">Review previous risk audits and safety reports</p>
        </div>
        <Link href="/app/upload">
          <Button size="sm" className="gap-2">
            <PlusCircle size={14} />
            New analysis
          </Button>
        </Link>
      </div>

      <div className="flex gap-4">
         <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={14} />
            <input 
              type="text" 
              placeholder="Filter by scene name or job ID..." 
              className="bg-surface border border-border rounded-md pl-9 pr-4 py-2 text-sm w-full focus:ring-1 focus:ring-accent outline-none" 
            />
         </div>
         <Button variant="outline" size="sm">Export CSV</Button>
      </div>

      <div className="rounded-md border border-border overflow-hidden bg-surface/30">
        <table className="w-full text-left text-xs">
          <thead className="bg-surface text-zinc-500 uppercase font-medium tracking-wider border-b border-border">
            <tr>
              <th className="p-4">Date</th>
              <th className="p-4">Scene</th>
              <th className="p-4">Objects</th>
              <th className="p-4">Collision-Free</th>
              <th className="p-4 font-mono">G-SAFE Avg</th>
              <th className="p-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {DEMO_ANALYSES.map((row) => (
              <tr 
                key={row.id} 
                className="hover:bg-surface/50 cursor-pointer transition-colors group"
                onClick={() => {}}
              >
                <td className="p-4 text-zinc-400 font-mono">{row.date}</td>
                <td className="p-4 text-zinc-200 font-medium group-hover:text-accent font-mono truncate max-w-[200px]">{row.scene}</td>
                <td className="p-4 text-zinc-400">{row.objects}</td>
                <td className={cn(
                  "p-4 font-medium",
                  parseInt(row.colFree) > 70 ? "text-success" : "text-warning"
                )}>{row.colFree}</td>
                <td className="p-4 text-zinc-300 font-mono">{row.safeAvg}</td>
                <td className="p-4">
                  <Badge variant="secondary" className="bg-zinc-800 text-zinc-300 text-[9px]">{row.status}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function cn(...inputs: any[]) { return inputs.filter(Boolean).join(" "); }
