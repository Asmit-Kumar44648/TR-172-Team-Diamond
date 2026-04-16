"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, FileCode, CheckCircle, ChevronDown, ChevronUp } from "lucide-react";
import { uploadScene, runAnalysis } from "@/lib/api";
import { cn } from "@/lib/utils";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  // Gripper Config
  const [jawWidth, setJawWidth] = useState([85]);
  const [maxAperture, setMaxAperture] = useState([80]);
  
  // Advanced Options
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [config, setConfig] = useState({
    enable_tda: false,
    enable_sim: true,
    top_n: 10
  });

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) setFile(droppedFile);
  };

  const handleRun = async () => {
    if (!file) return;
    setIsUploading(true);
    try {
      // 1. Upload
      const uploadRes = await uploadScene(file, jawWidth[0], maxAperture[0]);
      
      // 2. Trigger Analysis
      const analysisRes = await runAnalysis(uploadRes.scene_id, config);
      
      // 3. Navigate
      router.push(`/app/analysis/${analysisRes.job_id}`);
    } catch (err) {
      console.error(err);
      setIsUploading(false);
    }
  };

  const useDemo = (name: string) => {
    // For demo mode we'll just simulate a selection
    alert(`Demo scene ${name} selected. In a real integration this would load a preset .npz from the server.`);
  };

  return (
    <div className="max-w-2xl mx-auto py-12 px-6">
      <div className="space-y-8">
        <div>
          <h1 className="text-sm font-medium text-zinc-200 tracking-wide uppercase mb-8">Begin Analysis</h1>
          
          {/* Upload Zone */}
          <div 
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            className={cn(
              "border-2 border-dashed rounded-lg p-12 text-center transition-colors cursor-pointer",
              file ? "border-accent bg-accent/5" : "border-zinc-700 hover:border-zinc-500 bg-surface/50"
            )}
          >
            <input 
              type="file" 
              className="hidden" 
              id="file-upload" 
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              accept=".npz,.npy,.png"
            />
            <label htmlFor="file-upload" className="cursor-pointer block">
              <Upload className={cn("mx-auto h-12 w-12 mb-4", file ? "text-accent" : "text-zinc-600")} />
              {file ? (
                <div className="space-y-2">
                  <p className="text-sm text-zinc-100 font-medium">{file.name}</p>
                  <p className="text-xs text-zinc-500 font-mono">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <p className="text-sm text-zinc-300">Drop your depth scene map here</p>
                  <p className="text-xs text-zinc-500 uppercase tracking-wider">.NPZ, .NPY, or 16-BIT .PNG</p>
                </div>
              )}
            </label>
          </div>

          {/* Demo Scene Tabs */}
          <div className="mt-4 flex items-center gap-2">
            <span className="text-xs text-zinc-500 mr-2 uppercase tracking-tight">DEMO:</span>
            {["Easy", "Medium", "Cluttered bin"].map((d) => (
              <button 
                key={d} 
                onClick={() => useDemo(d)}
                className="text-xs bg-surface border border-border px-3 py-1.5 rounded-sm text-zinc-400 hover:text-zinc-100 transition-colors"
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Gripper Config */}
        <section className="space-y-6">
          <div className="flex items-center gap-2">
            <span className="h-px bg-border flex-1" />
            <h2 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Gripper Configuration</h2>
            <span className="h-px bg-border flex-1" />
          </div>

          <div className="grid gap-8">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label className="text-sm text-zinc-300">Jaw Width</label>
                <span className="text-sm font-mono text-accent">{jawWidth[0]}mm</span>
              </div>
              <Slider 
                value={jawWidth} 
                onValueChange={setJawWidth} 
                max={120} 
                min={40} 
                step={1} 
              />
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label className="text-sm text-zinc-300">Max Aperture</label>
                <span className="text-sm font-mono text-accent">{maxAperture[0]}mm</span>
              </div>
              <Slider 
                value={maxAperture} 
                onValueChange={setMaxAperture} 
                max={150} 
                min={20} 
                step={1} 
              />
            </div>
          </div>
        </section>

        {/* Advanced Options */}
        <div className="border border-border rounded-lg overflow-hidden">
          <button 
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="w-full flex justify-between items-center p-4 bg-surface text-xs font-medium text-zinc-400 hover:text-zinc-200 transition-colors"
          >
            ADVANCED OPTIONS
            {showAdvanced ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
          
          {showAdvanced && (
            <div className="p-4 bg-background border-t border-border space-y-4">
               <div className="flex items-center justify-between">
                  <label className="text-xs text-zinc-400">ENABLE TOPOLOGICAL DATA ANALYSIS (TDA)</label>
                  <input 
                    type="checkbox" 
                    checked={config.enable_tda}
                    onChange={(e) => setConfig({...config, enable_tda: e.target.checked})}
                    className="accent-accent"
                  />
               </div>
               <div className="flex items-center justify-between">
                  <label className="text-xs text-zinc-400">ENABLE PHYSICS SIMULATION VALIDATION</label>
                  <input 
                    type="checkbox" 
                    checked={config.enable_sim}
                    onChange={(e) => setConfig({...config, enable_sim: e.target.checked})}
                    className="accent-accent"
                  />
               </div>
               <div className="flex items-center justify-between">
                  <label className="text-xs text-zinc-400">TOP-N GRASPS TO RANK</label>
                  <input 
                    type="number" 
                    value={config.top_n}
                    onChange={(e) => setConfig({...config, top_n: parseInt(e.target.value)})}
                    className="bg-surface border border-border rounded text-xs p-1 w-12 font-mono text-center"
                  />
               </div>
            </div>
          )}
        </div>

        <Button 
          onClick={handleRun} 
          disabled={!file || isUploading}
          className="w-full h-12 text-sm font-semibold tracking-wide"
        >
          {isUploading ? "PROCESS_RUNNING..." : "RUN ANALYSIS"}
        </Button>
      </div>
    </div>
  );
}
