interface AgentBriefProps {
  summary: string | null;
  status: string;
}

export default function AgentBrief({ summary, status }: AgentBriefProps) {
  const isLoading = status !== 'COMPLETE' && !summary;

  return (
    <div className="space-y-3">
      <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">
        Scene Brief
      </div>
      
      {isLoading ? (
        <div className="space-y-2 py-1">
          <div className="h-3 w-full bg-zinc-800 animate-pulse rounded-sm" />
          <div className="h-3 w-[180px] bg-zinc-800 animate-pulse rounded-sm" />
          <div className="h-3 w-[220px] bg-zinc-800 animate-pulse rounded-sm" />
        </div>
      ) : (
        <p className="text-sm text-zinc-300 leading-relaxed italic">
          {summary || "Waiting for auditor analysis..."}
        </p>
      )}
    </div>
  );
}
