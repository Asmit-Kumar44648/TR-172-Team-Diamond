"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

const SECTIONS = [
  { id: "quickstart", title: "Quickstart" },
  { id: "upload", title: "Upload API" },
  { id: "analysis", title: "Analysis API" },
  { id: "schema", title: "Result Schema" },
  { id: "scores", title: "Score Explanations" },
  { id: "ros", title: "ROS MoveIt Guide" },
  { id: "webhooks", title: "Webhooks" },
  { id: "sdk", title: "Python SDK" },
  { id: "benchmark", title: "Methodology" },
];

export default function DocsPage() {
  const [active, setActive] = useState("quickstart");

  return (
    <div className="flex h-screen overflow-hidden">
      <aside className="w-64 border-r border-border bg-background p-6 overflow-y-auto">
        <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-6 px-3">Documentation</div>
        <nav className="space-y-1">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              onClick={() => setActive(s.id)}
              className={cn(
                "w-full text-left px-3 py-2 text-xs font-medium rounded-md transition-colors",
                active === s.id ? "bg-surface text-accent" : "text-zinc-500 hover:text-zinc-300"
              )}
            >
              {s.title}
            </button>
          ))}
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto p-12 bg-background">
        <div className="max-w-3xl space-y-8">
          {active === "quickstart" && (
            <article className="space-y-4">
              <h1 className="text-2xl font-semibold text-zinc-100 italic">Quickstart Guide</h1>
              <p className="text-zinc-400 text-sm leading-relaxed">
                Download your depth scene and authorize your first grasp in under 3 minutes.
              </p>
              
              <div className="space-y-2 pt-4">
                <h3 className="text-xs font-bold text-zinc-200 uppercase">1. Install the SDK</h3>
                <div className="bg-surface border border-border rounded-sm p-4 font-mono text-[11px] text-zinc-400">
                  pip install grasp-python-sdk
                </div>
              </div>

              <div className="space-y-2 pt-4">
                <h3 className="text-xs font-bold text-zinc-200 uppercase">2. Authenticate</h3>
                <div className="bg-surface border border-border rounded-sm p-4 font-mono text-[11px] text-zinc-400">
                  export GRASP_API_KEY="grsp_live_xxxxxxxxx"
                </div>
              </div>

              <div className="space-y-2 pt-4">
                <h3 className="text-xs font-bold text-zinc-200 uppercase">3. Upload & Run</h3>
                <div className="bg-surface border border-border rounded-sm p-4 font-mono text-[11px] text-zinc-400">
                  {`import grasp\n\nscene = grasp.Scene.from_npz("path/to/depth.npz")\njob = scene.analyze(jaw_width=85)\n\nfor event in job.stream():\n    print(f"[{event.progress}%] {event.stage}")\n\nprint("Reliability Audit:", job.result.top_10_grasps[0].audit.explanation)`}
                </div>
              </div>
            </article>
          )}

          {active !== "quickstart" && (
            <div className="flex flex-col items-center justify-center py-20 text-zinc-600 border border-dashed border-zinc-800 rounded-lg">
               <span className="text-xs uppercase font-medium">Section Content Placeholder</span>
               <span className="text-[10px] mt-2 italic">Detailed MDX documentation for "{active}" is being generated.</span>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
