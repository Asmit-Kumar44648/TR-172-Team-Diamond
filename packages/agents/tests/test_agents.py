import pytest
import asyncio
import json
from unittest.mock import MagicMock, patch

from packages.agents.agents import call_ranker, call_explainer_batch, call_summariser, run_all_agents

# Dummy grasp payloads
mock_grasps = [{"rank": 1, "rejected": False} for _ in range(10)]
mock_pipeline_result = {"top_10_grasps": mock_grasps, "object_count": 5}

class MockMessageResponse:
    def __init__(self, text):
         self.text = text
         
class MockAnthropicResponse:
    def __init__(self, text):
         self.content = [MockMessageResponse(text)]

@pytest.mark.asyncio
@patch("packages.agents.agents.client.messages.create")
async def test_call_ranker_parses_json(mock_create):
    # Anthropic response payload wrapped in markdown
    mock_json = """```json
[
    {"rank": 1, "grasp_id": "g0", "reasoning": "Solid"}
]
```"""
    mock_create.return_value = MockAnthropicResponse(mock_json)
    
    result = await call_ranker(mock_grasps)
    assert len(result) == 1
    assert result[0]["reasoning"] == "Solid"

@pytest.mark.asyncio
@patch("packages.agents.agents.client.messages.create")
async def test_call_explainer_batch_padding(mock_create):
    # Return fewer than 10 explanations
    mock_json = """[
        "Reason 1.", "Reason 2."
    ]"""
    mock_create.return_value = MockAnthropicResponse(mock_json)
    
    result = await call_explainer_batch(mock_grasps)
    assert len(result) == 10
    assert result[0] == "Reason 1."
    assert result[2] == "Analysis unavailable"
    assert result[9] == "Analysis unavailable"

@pytest.mark.asyncio
@patch("packages.agents.agents.call_ranker")
@patch("packages.agents.agents.call_explainer_batch")
@patch("packages.agents.agents.call_summariser")
async def test_run_all_agents_error_handling(mock_summ, mock_expl, mock_rank):
    # Simulate an agent crashing completely
    mock_summ.side_effect = Exception("Anthropic API Down")
    mock_expl.return_value = ["Fine"] * 10
    mock_rank.return_value = [{"rank": 1}]
    
    result = await run_all_agents(mock_pipeline_result)
    
    assert "scene_summary" in result
    assert "per_grasp_explanations" in result
    assert "agent_reranking" in result
    
    # Check gracefull falbback logic
    assert result["scene_summary"] == "Analysis unavailable"
    assert len(result["per_grasp_explanations"]) == 10
    assert result["agent_reranking"][0]["rank"] == 1

@pytest.mark.asyncio
async def test_agent_concurrency_blocks():
    from packages.agents.streaming import stream_agent_results
    import inspect
    
    # Assert stream logic yields asynchronously
    gen = stream_agent_results(mock_pipeline_result)
    assert inspect.isasyncgen(gen)
