import anthropic
import asyncio
import json
from typing import Optional

# Explicitly as requested by the instructions
client = anthropic.Anthropic()

SYSTEM_RANKER = """You are a robotic manipulation safety expert with 
20 years of industrial bin-picking experience. You evaluate grasp 
candidates for production deployment — not research benchmarks.
You think about: what happens if this grasp fails? Can the robot recover? 
Does removing this object destabilize the rest of the bin?
A cascade failure (Type-K) is 10x more costly than a slip (Type-S).
If any score is unavailable or NaN, state that explicitly — never invent data."""

SYSTEM_EXPLAINER = """You write safety assessments for factory-floor 
supervisors. Your reader is standing next to a robot arm, on a tablet,
about to approve or reject an action. They are NOT engineers. 
Write ONE sentence, maximum 20 words, in plain English.
No numbers. No acronyms. No technical jargon.
GOOD: "Clear approach from above — stable surface, nothing will topple when this piece is removed."
BAD: "The G-SAFE score of 0.82 indicates low composite failure risk across Type-S/C/O/R dimensions."
Only output the sentence. Nothing else."""

SYSTEM_SUMMARISER = """You are an industrial robotics analyst briefing 
a warehouse operations manager. 4 sentences maximum. Plain English.
Cover: what objects are visible, the primary picking challenge,
which region to clear first and why, any cascade risks.
Write as if you are handing this to someone about to supervise 
a robot arm. Only output the paragraph. No headers. No bullets."""

MODEL_NAME = "claude-sonnet-4-20250514"

async def call_ranker(grasps: list) -> Optional[list]:
    """
    Sends top-10 grasp scores + flags to Claude.
    Returns JSON array: [{rank, grasp_id, reasoning}]
    """
    payload = []
    for idx, g in enumerate(grasps):
        audit = g.get("audit", {})
        payload.append({
            "rank": g.get("rank", idx+1),
            "grasp_id": g.get("grasp", {}).get("grasp_id", f"g{idx}"),
            "scores": {
                 "s": audit.get("s_score"), "c": audit.get("c_score"), 
                 "o": audit.get("o_score"), "r": audit.get("r_score"), 
                 "k": audit.get("k_score"), "tci": audit.get("tci_score"), 
                 "gtv": audit.get("gtv_score"), "g_safe": audit.get("g_safe")
            },
            "flags": audit.get("flags", []),
            "rejected": g.get("rejected", False)
        })

    prompt_text = f"Review these grasps and re-rank them based on safety, heavily weighting Cascade (K) over slip.\nPayload:\n{json.dumps(payload, indent=2)}\nReturn ONLY a JSON array."
    
    try:
        # Wrap the sync client execution in an async thread pool to prevent blocking
        response = await asyncio.to_thread(
             client.messages.create,
             model=MODEL_NAME,
             max_tokens=800,
             system=SYSTEM_RANKER,
             messages=[{"role": "user", "content": prompt_text}]
        )
        content = response.content[0].text.strip()
        
        # Strip potential markdown fences
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            content = "\n".join(lines).strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Ranker error: {e}")
        return None

async def call_explainer_batch(grasps: list) -> list:
    """
    Sends all 10 grasps in ONE API call.
    Returns array of exactly 10 strings.
    """
    payload = []
    for idx, g in enumerate(grasps):
        audit = g.get("audit", {})
        payload.append({
            "grasp_number": idx + 1,
            "flags": audit.get("flags", []),
            "rejected": g.get("rejected", False),
            "reason": audit.get("rejection_reason", ""),
            "g_safe": audit.get("g_safe"),
            "cascade_risk": audit.get("k_score"),
            "slip_risk": audit.get("s_score")
        })

    prompt_text = f"Write an explainer for each of these {len(payload)} grasps. Return ONLY a JSON array of plain strings.\nPayload:\n{json.dumps(payload, indent=2)}"
    
    try:
        response = await asyncio.to_thread(
             client.messages.create,
             model=MODEL_NAME,
             max_tokens=600,
             system=SYSTEM_EXPLAINER,
             messages=[{"role": "user", "content": prompt_text}]
        )
        content = response.content[0].text.strip()
        
        # Strip markdown fences
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            content = "\n".join(lines).strip()
            
        explanations = json.loads(content)
        if not isinstance(explanations, list):
            raise ValueError("Expected a JSON array")
            
    except Exception as e:
        print(f"Explainer error: {e}")
        explanations = []
        
    # Ensure exactly 10 strings are returned
    while len(explanations) < 10:
        explanations.append("Analysis unavailable")
        
    return explanations[:10]

async def call_summariser(pipeline_result: dict) -> str:
    """
    Creates a 4 sentence high-level summary.
    """
    grasps = pipeline_result.get("top_10_grasps", [])
    has_rank1_rejected = any(g.get("rank") == 1 and g.get("rejected") for g in grasps)
    rejection_reasons = [g.get("audit", {}).get("rejection_reason") for g in grasps if g.get("rejected")]
    high_cascade = sum(1 for g in grasps if g.get("audit", {}).get("k_score", 0) > 0.5)
    avg_g_safe = sum(g.get("audit", {}).get("g_safe", 0) for g in grasps) / max(1, len(grasps))
    
    context = {
        "object_count": pipeline_result.get("object_count", 0),
        "entropy": 0.5, # Dummy value placeholder
        "collision_free_ratio": pipeline_result.get("collision_free_ratio", 1.0),
        "rank1_rejected": has_rank1_rejected,
        "rejection_reason": rejection_reasons[0] if rejection_reasons else None,
        "high_cascade_objects": high_cascade,
        "avg_g_safe": avg_g_safe
    }
    
    prompt_text = f"Write the briefing based on this context:\n{json.dumps(context, indent=2)}"
    
    try:
        response = await asyncio.to_thread(
             client.messages.create,
             model=MODEL_NAME,
             max_tokens=200,
             system=SYSTEM_SUMMARISER,
             messages=[{"role": "user", "content": prompt_text}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"Summariser error: {e}")
        return "Analysis unavailable due to system error."


async def run_all_agents(pipeline_result: dict) -> dict:
    """
    Executes all three agents concurrently without raising exceptions to the caller.
    """
    grasps = pipeline_result.get("top_10_grasps", [])
    
    results = await asyncio.gather(
        call_summariser(pipeline_result),
        call_explainer_batch(grasps),
        call_ranker(grasps),
        return_exceptions=True
    )
    
    summary_res = results[0] if not isinstance(results[0], Exception) else "Analysis unavailable"
    expl_res = results[1] if not isinstance(results[1], Exception) else ["Analysis unavailable"] * 10
    rank_res = results[2] if not isinstance(results[2], Exception) else None
    
    return {
        "scene_summary": summary_res,
        "per_grasp_explanations": expl_res,
        "agent_reranking": rank_res
    }
