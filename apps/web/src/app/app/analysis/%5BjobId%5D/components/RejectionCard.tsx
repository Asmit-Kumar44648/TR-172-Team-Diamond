interface RejectionCardProps {
  reason?: string | null;
  promotedRank?: number;
}

export default function RejectionCard({ reason, promotedRank }: RejectionCardProps) {
  return (
    <div className="bg-red-950/20 border border-red-900/40 p-4 rounded-sm space-y-2">
      <div className="text-[10px] font-bold uppercase tracking-widest text-amber-500">
        ⚠ RANK-1 OVERRIDDEN
      </div>
      
      <p className="text-sm text-zinc-300">
        {reason || "Grasp failed safety audit criteria."}
      </p>
      
      {promotedRank && (
        <div className="text-[10px] font-bold text-success uppercase">
          Operational recommendation: Rank {promotedRank}
        </div>
      )}
    </div>
  );
}
