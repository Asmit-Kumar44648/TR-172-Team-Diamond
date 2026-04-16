import asyncio
import json

async def stream_agent_results(pipeline_result: dict):
    """
    Async generator that streams SSE formats for agent tasks execution concurrently.
    """
    grasps = pipeline_result.get("top_10_grasps", [])
    
    # Imports inside block to avoid circular issues during testing if necessary
    from .agents import call_summariser, call_explainer_batch, call_ranker
    
    yield f'data: {json.dumps({"type": "agent_start"})}\n\n'
    
    # We create wrapped tasks to emit their specific 'type' when they finish
    async def run_summariser():
        res = await call_summariser(pipeline_result)
        return {"type": "scene_summary", "content": res}
        
    async def run_explainer():
        res = await call_explainer_batch(grasps)
        return {"type": "explanations", "content": res}
        
    async def run_ranker():
        res = await call_ranker(grasps)
        return {"type": "reranking", "content": res}
        
    tasks = [
        asyncio.create_task(run_summariser()),
        asyncio.create_task(run_explainer()),
        asyncio.create_task(run_ranker())
    ]
    
    for completed_task in asyncio.as_completed(tasks):
        try:
            result = await completed_task
            yield f'data: {json.dumps(result)}\n\n'
        except Exception as e:
            # On generic catastrophic error
            yield f'data: {json.dumps({"type": "error", "message": f"Agent stream failure: {str(e)}"})}\n\n'
            
    yield f'data: {json.dumps({"type": "agents_complete"})}\n\n'
