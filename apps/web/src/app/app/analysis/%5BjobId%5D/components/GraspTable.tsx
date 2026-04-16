import { GraspRecord } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface GraspTableProps {
  grasps: GraspRecord[];
  selectedIndex: number | null;
  onSelectGrasp: (index: number | null) => void;
}

const SCORE_LABELS = ['S', 'C', 'O', 'R', 'K'];

function ScoreBar({ value }: { value: number }) {
  // Height 20px, width 2px
  const h = Math.max(2, Math.min(20, value * 20));
  const color = value > 0.6 ? "bg-danger" : value > 0.35 ? "bg-warning" : "bg-success";
  return (
    <div className="flex flex-col justify-end h-[20px] w-[2px] bg-zinc-800 rounded-full overflow-hidden">
      <div className={cn("w-full transition-all duration-500", color)} style={{ height: `${h}px` }} />
    </div>
  );
}

export default function GraspTable({ grasps, selectedIndex, onSelectGrasp }: GraspTableProps) {
  return (
    <TooltipProvider>
      <div className="w-full">
        <table className="w-full border-collapse text-[10px] text-zinc-500 text-left">
          <thead className="sticky top-0 bg-background/95 backdrop-blur-sm z-20 border-b border-border">
            <tr className="uppercase tracking-wider">
              <th className="p-2 font-medium">#</th>
              <th className="p-2 font-medium">Safe</th>
              <th className="p-2 font-medium text-center">S C O R K</th>
              <th className="p-2 font-medium">Status</th>
              <th className="p-2 font-medium">Explanation</th>
            </tr>
          </thead>
          <tbody>
            {grasps.map((g, i) => {
              const a = g.audit;
              const isSelected = selectedIndex === i;
              const isRejected = g.rejected;
              const isOperational = g.is_operational;

              return (
                <tr 
                  key={g.grasp.grasp_id}
                  onClick={() => onSelectGrasp(i)}
                  className={cn(
                    "group cursor-pointer border-b border-border/50 transition-colors",
                    isSelected ? "bg-accent/10" : "hover:bg-surface/50",
                    isRejected ? "bg-red-950/5 border-l-2 border-l-danger/50" : 
                    isOperational ? "border-l-2 border-l-success/50" : ""
                  )}
                >
                  <td className={cn("p-2 font-mono", isRejected && "line-through text-zinc-600")}>
                    {g.rank}
                  </td>
                  
                  <td className={cn(
                    "p-2 font-mono text-xs",
                    a.g_safe > 0.7 ? "text-success" : a.g_safe > 0.4 ? "text-warning" : "text-danger"
                  )}>
                    {a.g_safe.toFixed(3)}
                  </td>

                  <td className="p-2">
                    <div className="flex justify-center gap-[2px]">
                      <ScoreBar value={a.s_score} />
                      <ScoreBar value={a.c_score} />
                      <ScoreBar value={a.o_score} />
                      <ScoreBar value={a.r_score} />
                      <ScoreBar value={a.k_score} />
                    </div>
                  </td>

                  <td className="p-2 uppercase font-bold text-[9px]">
                    {isRejected ? (
                      <span className="text-danger flex items-center gap-1">✕ REJECT</span>
                    ) : (
                      <span className="text-success flex items-center gap-1">✓ OK</span>
                    )}
                  </td>

                  <td className="p-2 max-w-[120px]">
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <div className="truncate text-zinc-400 group-hover:text-zinc-200">
                          {a.explanation || "No audit details available."}
                        </div>
                      </TooltipTrigger>
                      <TooltipContent side="left" className="max-w-[300px] bg-zinc-900 border-zinc-700 text-xs">
                        {a.explanation}
                        {a.flags.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {a.flags.map(f => <span key={f} className="bg-red-950 text-red-400 px-1 rounded-sm border border-red-900">{f}</span>)}
                          </div>
                        )}
                      </TooltipContent>
                    </Tooltip>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </TooltipProvider>
  );
}
