"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { useAnalysisStore } from "@/stores/analysisStore";
import { useAnalysisStream } from "@/hooks/useAnalysisStream";
import { cn } from "@/lib/utils";

// Sub-components
import StatusHeader from "./components/StatusHeader";
import AgentBrief from "./components/AgentBrief";
import MetricsSummary from "./components/MetricsSummary";
import RejectionCard from "./components/RejectionCard";
import ThreeViewer from "./components/ThreeViewer";
import GraspTable from "./components/GraspTable";

export default function AnalysisPage() {
  const { jobId } = useParams() as { jobId: string };
  const store = useAnalysisStore();
  
  // Hook up SSE stream
  useAnalysisStream(jobId);

  // Auto-select rank 1 on completion
  useEffect(() => {
    if (store.status === "COMPLETE" && store.result && store.selectedGraspIndex === null) {
      store.selectGrasp(0);
    }
  }, [store.status, store.result]);

  return (
    <div className="flex h-screen overflow-hidden text-zinc-300">
      
      {/* ── LEFT PANEL (280px) ── */}
      <aside className="w-[280px] flex-shrink-0 border-r border-border flex flex-col bg-background">
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          <StatusHeader 
            status={store.status} 
            stage={store.stage} 
            progress={store.progress} 
            inferenceTime={store.result?.inference_time_seconds}
          />
          
          <div className="h-px bg-border" />
          
          <AgentBrief 
            summary={store.agentData.summary} 
            status={store.status}
          />
          
          <div className="h-px bg-border" />
          
          <MetricsSummary 
            collisionFree={store.result?.collision_free_count}
            objectCount={store.result?.object_count}
            avgGSafe={store.result ? (store.result.top_10_grasps.reduce((acc, g) => acc + g.audit.g_safe, 0) / store.result.top_10_grasps.length).toFixed(3) : null}
          />
          
          {store.result && store.result.top_10_grasps[0]?.rejected && (
            <RejectionCard 
              reason={store.result.top_10_grasps[0].audit.rejection_reason}
              promotedRank={store.result.top_10_grasps.find(g => !g.rejected)?.rank}
            />
          )}
        </div>
      </aside>

      {/* ── CENTER PANEL (Flexible) ── */}
      <main className="flex-1 flex flex-col relative bg-[#0d0d0f]">
        <div className="absolute top-4 left-4 z-10 flex gap-1 p-1 bg-surface/80 rounded-md border border-border backdrop-blur-sm">
          {['3D View', 'Segmentation', 'Depth'].map((mode) => (
            <button
              key={mode}
              onClick={() => store.setViewerMode(mode.toLowerCase().slice(0,3) as any)}
              className={cn(
                "px-3 py-1 text-[10px] uppercase font-semibold tracking-wider rounded-sm transition-colors",
                store.viewerMode === mode.toLowerCase().slice(0,3) 
                  ? "bg-zinc-100 text-zinc-950" 
                  : "text-zinc-500 hover:text-zinc-200"
              )}
            >
              {mode}
            </button>
          ))}
        </div>
        
        <div className="flex-1 relative">
           <ThreeViewer 
             mode={store.viewerMode} 
             grasps={store.result?.top_10_grasps || []}
             selectedIndex={store.selectedGraspIndex}
             onSelectGrasp={store.selectGrasp}
           />
        </div>
      </main>

      {/* ── RIGHT PANEL (360px) ── */}
      <aside className="w-[360px] flex-shrink-0 border-l border-border bg-background flex flex-col">
        <div className="flex-1 overflow-y-auto">
          <GraspTable 
            grasps={store.result?.top_10_grasps || []}
            selectedIndex={store.selectedGraspIndex}
            onSelectGrasp={store.selectGrasp}
          />
        </div>
        
        {/* Actions Footer */}
        <div className="p-4 border-t border-border bg-surface/30 space-y-2">
          <Button className="w-full text-xs" disabled={store.status !== 'COMPLETE'}>
            Download ROS JSON
          </Button>
          <div className="grid grid-cols-2 gap-2">
             <Button variant="outline" className="text-xs" disabled={store.status !== 'COMPLETE'}>Report</Button>
             <Button variant="outline" className="text-xs" disabled={store.status !== 'COMPLETE'}>Share</Button>
          </div>
        </div>
      </aside>
    </div>
  );
}
