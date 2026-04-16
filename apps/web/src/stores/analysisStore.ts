import { create } from 'zustand';
import { ScenePlan } from '@/lib/types';

interface AgentData {
  summary: string | null;
  explanations: string[] | null;
  reranking: { rank: number; grasp_id: string; reasoning: string }[] | null;
}

interface AnalysisState {
  currentJobId: string | null;
  status: 'IDLE' | 'QUEUED' | 'RUNNING' | 'COMPLETE' | 'FAILED';
  progress: number;
  stage: string;
  result: ScenePlan | null;
  agentData: AgentData;
  error: string | null;
  
  // UI State
  selectedGraspIndex: number | null;
  viewerMode: '3d' | 'seg' | 'depth';
  
  // Actions
  setJobFlow: (jobId: string, status: string) => void;
  updateProgress: (stage: string, progress: number) => void;
  setResult: (result: ScenePlan) => void;
  updateAgentData: (key: keyof AgentData, content: any) => void;
  fail: (error: string) => void;
  reset: () => void;
  
  setViewerMode: (mode: '3d' | 'seg' | 'depth') => void;
  selectGrasp: (index: number | null) => void;
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  currentJobId: null,
  status: 'IDLE',
  progress: 0,
  stage: 'Waiting...',
  result: null,
  agentData: { summary: null, explanations: null, reranking: null },
  error: null,
  
  selectedGraspIndex: null,
  viewerMode: '3d',

  setJobFlow: (jobId, status) => set({ currentJobId: jobId, status: status as any, error: null }),
  updateProgress: (stage, progress) => set({ stage, progress, status: progress === 100 ? 'COMPLETE' : 'RUNNING' }),
  setResult: (result) => set({ result, status: 'COMPLETE', progress: 100 }),
  updateAgentData: (key, content) => set((state) => ({ agentData: { ...state.agentData, [key]: content } })),
  fail: (error) => set({ status: 'FAILED', error }),
  reset: () => set({ 
    currentJobId: null, status: 'IDLE', progress: 0, stage: 'Waiting...', 
    result: null, error: null, agentData: { summary: null, explanations: null, reranking: null } 
  }),
  
  setViewerMode: (viewerMode) => set({ viewerMode }),
  selectGrasp: (selectedGraspIndex) => set({ selectedGraspIndex }),
}));
