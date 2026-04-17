"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PlusCircle, Search, Activity, ShieldAlert, CheckCircle2 } from "lucide-react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

const DEMO_ANALYSES = [
  { id: "job-001", date: "2026-04-16", scene: "bin_picking_01.npz", objects: 5, colFree: "80%", safeAvg: "0.824", status: "COMPLETE" },
  { id: "job-002", date: "2026-04-15", scene: "random_clutter.npz", objects: 12, colFree: "42%", safeAvg: "0.451", status: "COMPLETE" },
  { id: "job-003", date: "2026-04-14", scene: "clear_table.npy", objects: 2, colFree: "100%", safeAvg: "0.912", status: "COMPLETE" },
  { id: "job-004", date: "2026-04-13", scene: "dense_gears.npz", objects: 18, colFree: "28%", safeAvg: "0.315", status: "COMPLETE" },
  { id: "job-005", date: "2026-04-12", scene: "spilled_screws.npz", objects: 45, colFree: "15%", safeAvg: "0.198", status: "COMPLETE" },
];

const TREND_DATA = [
  { name: "Apr 12", gsafe: 0.198, col: 15 },
  { name: "Apr 13", gsafe: 0.315, col: 28 },
  { name: "Apr 14", gsafe: 0.912, col: 100 },
  { name: "Apr 15", gsafe: 0.451, col: 42 },
  { name: "Apr 16", gsafe: 0.824, col: 80 },
];

const TAXONOMY_DATA = [
  { name: "Slip (S)", score: 0.82 },
  { name: "Collision (C)", score: 0.45 },
  { name: "Obs (O)", score: 0.91 },
  { name: "Retract (R)", score: 0.64 },
  { name: "Cascade (K)", score: 0.33 },
];

export default function AnalysesPage() {
  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <div className="flex justify-between items-end border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-sm font-medium text-zinc-200 tracking-wide uppercase mb-1">Accumulated Analytics</h1>
          <p className="text-xs text-zinc-500 uppercase tracking-tight">Fleet-wide safety progression and G-SAFE taxonomy breakdowns</p>
        </div>
        <Link href="/app/upload">
          <Button size="sm" className="gap-2">
            <PlusCircle size={14} />
            New Audit
          </Button>
        </Link>
      </div>

      {/* Analytics Dashboard Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Graph */}
        <div className="lg:col-span-2 bg-surfaceElevated border border-border rounded-xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <Activity size={16} className="text-zinc-500" />
            <h3 className="text-xs font-bold text-zinc-300 uppercase tracking-widest">Fleet Mean G-SAFE Trend</h3>
          </div>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={TREND_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="name" stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} domain={[0, 1]} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', fontSize: '12px' }}
                  itemStyle={{ color: '#ffffff' }}
                />
                <Line type="monotone" dataKey="gsafe" stroke="#ffffff" strokeWidth={2} dot={{ fill: '#09090b', stroke: '#ffffff', strokeWidth: 2 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Taxonomy Bar */}
        <div className="bg-surfaceElevated border border-border rounded-xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <ShieldAlert size={16} className="text-zinc-500" />
            <h3 className="text-xs font-bold text-zinc-300 uppercase tracking-widest">Taxonomy Breakdown</h3>
          </div>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={TAXONOMY_DATA} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#52525b" fontSize={10} domain={[0, 1]} hide />
                <YAxis dataKey="name" type="category" stroke="#a1a1aa" fontSize={10} tickLine={false} axisLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', fontSize: '12px' }}
                  cursor={{ fill: '#18181b' }}
                />
                <Bar dataKey="score" fill="#ffffff" radius={[0, 4, 4, 0]} barSize={12} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
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
