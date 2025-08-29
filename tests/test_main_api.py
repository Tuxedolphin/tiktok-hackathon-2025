"""
Integration-like tests for main exposed API functions.
"""

import unittest
from typing import Any, Dict, List


class TestMainAPI(unittest.TestCase):
    def test_analyze_review_basic(self) -> None:
        from main import analyze_review

        result = analyze_review("Great food and excellent service.")
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get("success"))
        self.assertIn("trust_score", result)
        self.assertGreaterEqual(result["trust_score"], 0.0)
        self.assertLessEqual(result["trust_score"], 1.0)

    def test_analyze_bulk_reviews(self) -> None:
        from main import analyze_bulk_reviews

        data: List[Dict[str, Any]] = [
            {
                "text": "Amazing experience!",
                "reviewer_data": {"account_age_days": 100, "review_count": 10},
                "timestamp": "2025-08-20T00:00:00",
            },
            {
                "text": "Terrible service.",
                "reviewer_data": {"account_age_days": 10, "review_count": 1},
                "timestamp": "2025-08-21T00:00:00",
            },
        ]
        result = analyze_bulk_reviews(data)
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get("success"))
        self.assertIn("individual_results", result)
        self.assertEqual(len(result["individual_results"]), 2)

    def test_get_trust_dashboard_data(self) -> None:
        from main import get_trust_dashboard_data

        result = get_trust_dashboard_data("loc_123")
        self.assertTrue(result.get("success"))
        self.assertIn("trend_data", result)
        for item in result["trend_data"]:
            self.assertGreaterEqual(item["trust_score"], 0.0)
            self.assertLessEqual(item["trust_score"], 1.0)
            self.assertGreaterEqual(item["average_rating"], 1.0)
            self.assertLessEqual(item["average_rating"], 5.0)
