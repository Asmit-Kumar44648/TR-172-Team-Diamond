import unittest
from unittest.mock import MagicMock, patch
import io
import json
from grasp.client import GRASPClient
from grasp.models import ScenePlan
from grasp.exceptions import GRASPAuthError, GRASPRateLimitError

class TestGRASPClient(unittest.TestCase):
    def setUp(self):
        self.client = GRASPClient(api_key="test_key", base_url="http://mock-api.ai")

    @patch("httpx.Client.post")
    def test_analyze_sync_trigger(self, mock_post):
        # Mock responses for upload and run
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {"scene_id": "sc_123"}),
            MagicMock(status_code=200, json=lambda: {"job_id": "job_456"})
        ]
        
        # Mock wait() to not actually poll
        self.client.wait = MagicMock(return_value="mock_result")
        
        file_obj = io.BytesIO(b"dummy_npz")
        result = self.client.analyze(file_obj, wait=True)
        
        self.assertEqual(result, "mock_result")
        self.assertEqual(mock_post.call_count, 2)

    @patch("httpx.Client.get")
    def test_auth_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=401)
        
        with self.assertRaises(GRASPAuthError):
            self.client.get_usage()

    @patch("httpx.Client.get")
    def test_rate_limit_error(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=429, 
            json=lambda: {"detail": "Daily quota exceeded"}
        )
        
        with self.assertRaises(GRASPRateLimitError):
            self.client.get_usage()

    def test_ros_export(self):
        # Create a mock ScenePlan
        plan = ScenePlan(
            scene_id="s1", job_id="j1", timestamp="now",
            inference_time_seconds=1.0, collision_free_ratio=1.0,
            collision_free_count=1, object_count=1,
            top_10_grasps=[]
        )
        
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            plan.to_ros_json("test.json")
            mock_file.assert_called_once_with("test.json", "w")

if __name__ == "__main__":
    unittest.main()
