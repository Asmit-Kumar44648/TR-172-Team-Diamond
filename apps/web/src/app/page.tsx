import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center pt-32 pb-16 px-6">
      <div className="max-w-4xl w-full flex flex-col items-center text-center space-y-8">
        
        {/* Pre-Header Label */}
        <div className="text-xs font-semibold text-accent uppercase tracking-widest">
          GRASP RISK AUDIT & SAFETY PRE-FLIGHT
        </div>

        {/* Hero Section */}
        <h1 className="text-4xl font-bold text-foreground max-w-2xl leading-[1.1] tracking-tight">
          Audit robot grasps before the hardware moves.
        </h1>
        
        <p className="text-lg text-zinc-500 max-w-xl leading-relaxed">
          The industry's first open safety gate for robotic manipulation. Upload RGB-D scenes to generate, simulate, and audit grasp stability using the G-SAFE taxonomy.
        </p>

        {/* CTA */}
        <div className="flex items-center gap-4 pt-4">
          <Link href="/app/upload">
            <Button size="lg" className="px-10 h-12 text-base font-medium">Use Platform — It's Free</Button>
          </Link>
          <Link href="/app/docs">
            <Button size="lg" variant="outline" className="px-10 h-12 text-base border-border">Read the Paper</Button>
          </Link>
        </div>

        {/* Procedure Flow Section */}
        <div className="w-full max-w-4xl mt-32 pt-16 border-t border-zinc-100">
           <h2 className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-12">The Safety Procedure</h2>
           <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-left">
              <div className="space-y-3">
                 <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center font-bold text-sm">01</div>
                 <h4 className="font-semibold text-zinc-900">Scene Ingest</h4>
                 <p className="text-sm text-zinc-500 leading-relaxed">Raw RGB-D data is processed through SAM2 for industrial object segmentation.</p>
              </div>
              <div className="space-y-3">
                 <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center font-bold text-sm">02</div>
                 <h4 className="font-semibold text-zinc-900">Grasp Synthesis</h4>
                 <p className="text-sm text-zinc-500 leading-relaxed">Candidates are generated via Contact-GraspNet with geometric variance analysis.</p>
              </div>
              <div className="space-y-3">
                 <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center font-bold text-sm">03</div>
                 <h4 className="font-semibold text-zinc-900">G-SAFE Audit</h4>
                 <p className="text-sm text-zinc-500 leading-relaxed">Every pose is scored across the S/C/O/K taxonomy in a rigid-body physics simulator.</p>
              </div>
              <div className="space-y-3">
                 <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center font-bold text-sm">04</div>
                 <h4 className="font-semibold text-zinc-900">Agent Oversight</h4>
                 <p className="text-sm text-zinc-500 leading-relaxed">Claude-4 reviews final audit logs to provide natural language operation approval.</p>
              </div>
           </div>
        </div>

        {/* Comparison Section (G-SAFE Taxonomy) */}
        <div className="w-full max-w-4xl mt-32 bg-surfaceElevated rounded-2xl p-12 text-left border border-border">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
              <div>
                 <h3 className="text-2xl font-bold text-foreground mb-4">How we compare</h3>
                 <p className="text-muted-foreground leading-relaxed">Traditional models like AnyGrasp or Contact-GraspNet focus on "Success Probability." We focus on **"Consequence of Failure."**</p>
                 <div className="mt-8 space-y-4">
                    <div className="flex gap-4">
                       <div className="font-bold text-primary">S</div>
                       <div><span className="font-semibold text-zinc-300">Slip Risk:</span> Surface normal vs approach alignment.</div>
                    </div>
                    <div className="flex gap-4">
                       <div className="font-bold text-primary">C</div>
                       <div><span className="font-semibold text-zinc-300">Collision:</span> AABB intersection with clutter pointclouds.</div>
                    </div>
                    <div className="flex gap-4">
                       <div className="font-bold text-primary">O</div>
                       <div><span className="font-semibold text-zinc-300">Observation:</span> Depth repair uncertainty & camera noise.</div>
                    </div>
                    <div className="flex gap-4">
                       <div className="font-bold text-primary">K</div>
                       <div><span className="font-semibold text-zinc-300">Cascade:</span> Probability of the entire scene toppling.</div>
                    </div>
                 </div>
              </div>
              
              <div className="flex flex-col justify-center">
                 <div className="rounded-xl border border-border overflow-hidden bg-surface shadow-sm font-mono text-sm">
                    <div className="grid grid-cols-3 border-b border-border p-4 bg-zinc-900/50 text-zinc-400 text-xs font-bold uppercase tracking-wider">
                       <div>Metric</div>
                       <div>Contact-GN</div>
                       <div>GRASP</div>
                    </div>
                    <div className="grid grid-cols-3 border-b border-border p-4">
                       <div className="text-zinc-400">Seen AP</div>
                       <div className="text-zinc-500">69.9%</div>
                       <div className="text-foreground font-bold">73.6%</div>
                    </div>
                    <div className="grid grid-cols-3 border-b border-border p-4">
                       <div className="text-zinc-400">Unseen AP</div>
                       <div className="text-zinc-500">60.1%</div>
                       <div className="text-foreground font-bold">63.4%</div>
                    </div>
                    <div className="grid grid-cols-3 p-4">
                       <div className="text-zinc-400">Safety Gate</div>
                       <div className="text-red-500">No Audit</div>
                       <div className="text-primary font-bold">G-SAFE</div>
                    </div>
                 </div>
              </div>
           </div>
        </div>

        {/* Footer */}
        <div className="pt-24 text-zinc-400 text-xs">
           &copy; 2026 GRASP S.A.F.E Framework. Provided for industrial research & production safety.
        </div>

      </div>
    </div>
  );
}
