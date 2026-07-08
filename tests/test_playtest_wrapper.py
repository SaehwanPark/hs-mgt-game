import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from diagnose_runs import is_cash_retry  # noqa: E402
from play_game import normalize_tool_error  # noqa: E402


class PlaytestWrapperTests(unittest.TestCase):
  def test_normalize_tool_error_keeps_plain_string(self):
    self.assertEqual(
      normalize_tool_error("project budget 12 must be a multiple of duration 9 months"),
      {"error": "project budget 12 must be a multiple of duration 9 months"},
    )

  def test_normalize_tool_error_extracts_structured_fields(self):
    payload = json.dumps({
      "error": "cash required 25 exceeds available 10",
      "code": "insufficient_cash",
      "resource_limit": {
        "resource": "cash",
        "required": 25,
        "available": 10,
      },
      "hint": "Reduce cash spending before resubmitting.",
    })
    self.assertEqual(
      normalize_tool_error(payload),
      {
        "error": "cash required 25 exceeds available 10",
        "code": "insufficient_cash",
        "resource_limit": {
          "resource": "cash",
          "required": 25,
          "available": 10,
        },
        "hint": "Reduce cash spending before resubmitting.",
      },
    )

  def test_is_cash_retry_prefers_structured_metadata(self):
    self.assertTrue(is_cash_retry({
      "error": "not relied on",
      "code": "insufficient_cash",
      "resource_limit": {"resource": "cash", "required": 9, "available": 0},
    }))

  def test_is_cash_retry_falls_back_to_legacy_error_text(self):
    self.assertTrue(is_cash_retry({
      "error": "cash required 9 exceeds available 0",
    }))
    self.assertFalse(is_cash_retry({
      "error": "project budget 12 must be a multiple of duration 9 months",
    }))


if __name__ == "__main__":
  unittest.main()
