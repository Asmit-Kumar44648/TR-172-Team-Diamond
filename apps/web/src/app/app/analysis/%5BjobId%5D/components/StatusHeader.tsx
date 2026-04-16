import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface StatusHeaderProps {
  status: string;
  stage: string;
  progress: number;
  inferenceTime?: number;
}

export default function StatusHeader({ status, stage, progress, inferenceTime }: StatusHeaderProps) {
  const isComplete = status === 'COMPLETE';
  const isFailed = status === 'FAILED';

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Badge 
          variant={isComplete ? "success" : isFailed ? "destructive" : "secondary"}
          className="px-3"
        >
          {status}
        </Badge>
        {isComplete && inferenceTime && (
          <span className="text-[10px] font-mono text-zinc-500 uppercase">
            {inferenceTime.toFixed(2)}s Inference
          </span>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-[11px] font-medium uppercase tracking-wider">
          <span className="text-zinc-400">{isComplete ? "Job finalized" : stage}</span>
          <span className={cn(isComplete ? "text-success" : "text-accent")}>
            {progress}%
          </span>
        </div>
        <Progress value={progress} className="h-1" />
      </div>

      {isComplete && (
         <div className="text-[10px] font-mono text-zinc-500 text-center">
            Result authorized for deployment
         </div>
      )}
    </div>
  );
}
