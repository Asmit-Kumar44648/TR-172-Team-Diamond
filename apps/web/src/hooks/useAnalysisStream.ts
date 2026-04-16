import { useEffect } from 'react';
import { useAnalysisStore } from '@/stores/analysisStore';
import { StreamMessage } from '@/lib/types';
import { API_BASE } from '@/lib/api';

export function useAnalysisStream(jobId: string | null) {
  const store = useAnalysisStore();

  useEffect(() => {
    if (!jobId) return;

    store.setJobFlow(jobId, 'QUEUED');
    console.log(`[SSE] Connecting to ${jobId}...`);
    const sse = new EventSource(`${API_BASE}/analysis/${jobId}/stream`);

    sse.onmessage = (event) => {
      try {
        const msg: StreamMessage = JSON.parse(event.data);
        
        switch (msg.type) {
          case 'connected':
            console.log('[SSE] Connected.');
            break;
          case 'progress':
            if (msg.stage && msg.progress !== undefined) {
              store.updateProgress(msg.stage, msg.progress);
            }
            break;
          case 'complete':
            if (msg.result) {
              store.setResult(msg.result);
            }
            break;
          case 'scene_summary':
            store.updateAgentData('summary', msg.content);
            break;
          case 'explanations':
            store.updateAgentData('explanations', msg.content);
            break;
          case 'reranking':
            store.updateAgentData('reranking', msg.content);
            break;
          case 'error':
            store.fail(msg.message || 'Unknown error');
            sse.close();
            break;
          case 'agents_complete':
            console.log('[SSE] Agents complete, closing stream.');
            sse.close();
            break;
        }
      } catch (err) {
        console.error('SSE Parse Error', err);
      }
    };

    sse.onerror = () => {
      console.warn('[SSE] Stream closed or failed.');
      sse.close();
    };

    return () => {
      console.log(`[SSE] Unmounting, closing connection.`);
      sse.close();
    };
  }, [jobId]);
}
