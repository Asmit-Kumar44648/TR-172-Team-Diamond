interface MetricsSummaryProps {
  collisionFree?: number;
  objectCount?: number;
  avgGSafe?: string | null;
}

export default function MetricsSummary({ collisionFree, objectCount, avgGSafe }: MetricsSummaryProps) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <div className="text-[10px] font-medium text-zinc-500 uppercase tracking-wider mb-1">Obj Count</div>
          <div className="text-sm font-semibold text-zinc-200">{objectCount ?? "—"}</div>
        </div>
        <div>
          <div className="text-[10px] font-medium text-zinc-500 uppercase tracking-wider mb-1">Col-Free</div>
          <div className="text-sm font-semibold text-success">{collisionFree ?? "—"}</div>
        </div>
      </div>
      
      <div>
        <div className="text-[10px] font-medium text-zinc-500 uppercase tracking-wider mb-1">Avg G-SAFE</div>
        <div className="text-sm font-mono text-zinc-200">{avgGSafe ?? "—.———"}</div>
      </div>

      <div className="pt-2">
         <div className="text-[10px] font-mono text-zinc-500 leading-tight">
            Seen AP: 73.6% ✓<br/>
            Unseen AP: 63.4% ✓
         </div>
      </div>
    </div>
  );
}
