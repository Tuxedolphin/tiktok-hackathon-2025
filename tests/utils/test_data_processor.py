"""
Unit tests for the DataProcessor utility.
"""

import unittest
from typing import Dict, Any

from backend.utils.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for the DataProcessor class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.processor = DataProcessor()

    def test_initialisation(self) -> None:
        """Test that DataProcessor initialises correctly."""
        self.assertIsInstance(self.processor, DataProcessor)
        self.assertIsInstance(self.processor.sample_locations, list)
        self.assertIsInstance(self.processor.sample_review_texts, list)
        self.assertGreater(len(self.processor.sample_locations), 0)
        self.assertGreater(len(self.processor.sample_review_texts), 0)

    def test_generate_trend_data_default(self) -> None:
        """Test trend data generation with default parameters."""
        result = self.processor.generate_trend_data()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 30)  # Default 30 days

        for trend in result:
            self.assertIsInstance(trend, dict)
            self.assertIn("date", trend)
            self.assertIn("trust_score", trend)
            self.assertIn("review_count", trend)
            self.assertIn("average_rating", trend)

            self.assertGreaterEqual(trend["trust_score"], 0.0)
            self.assertLessEqual(trend["trust_score"], 1.0)
            self.assertGreaterEqual(trend["review_count"], 0)
            self.assertGreaterEqual(trend["average_rating"], 0.0)
            self.assertLessEqual(trend["average_rating"], 5.0)

    def test_generate_trend_data_custom_days(self) -> None:
        """Test trend data generation with custom number of days."""
        days = 7
        result = self.processor.generate_trend_data(days=days)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), days)

    def test_get_sample_trusted_reviews_default(self) -> None:
        """Test trusted reviews generation with default count."""
        result = self.processor.get_sample_trusted_reviews()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)  # Default count

        for review in result:
            self.assertIsInstance(review, dict)
            self.assertIn("id", review)
            self.assertIn("text", review)
            self.assertIn("trust_score", review)
            self.assertIn("rating", review)
            self.assertIn("date", review)
            self.assertIn("reviewer", review)

            self.assertGreaterEqual(review["trust_score"], 0.8)  # Should be high trust
            self.assertIn(review["rating"], [4, 5])  # Should be high ratings
            self.assertTrue(review["reviewer"]["verified"])  # Should be verified

    def test_get_sample_trusted_reviews_custom_count(self) -> None:
        """Test trusted reviews generation with custom count."""
        count = 10
        result = self.processor.get_sample_trusted_reviews(count=count)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), count)

    def test_get_sample_flagged_reviews_default(self) -> None:
        """Test flagged reviews generation with default count."""
        result = self.processor.get_sample_flagged_reviews()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # Default count

        for review in result:
            self.assertIsInstance(review, dict)
            self.assertIn("id", review)
            self.assertIn("text", review)
            self.assertIn("trust_score", review)
            self.assertIn("rating", review)
            self.assertIn("flags", review)

            self.assertLessEqual(review["trust_score"], 0.3)  # Should be low trust
            self.assertIn(review["rating"], [1, 5])  # Should be extreme ratings
            self.assertFalse(review["reviewer"]["verified"])  # Should not be verified

    def test_get_sample_flagged_reviews_custom_count(self) -> None:
        """Test flagged reviews generation with custom count."""
        count = 5
        result = self.processor.get_sample_flagged_reviews(count=count)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), count)

    def test_get_sample_reviewer_activity_default(self) -> None:
        """Test reviewer activity generation with default count."""
        result = self.processor.get_sample_reviewer_activity()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 10)  # Default count

        for activity in result:
            self.assertIsInstance(activity, dict)
            self.assertIn("date", activity)
            self.assertIn("type", activity)
            self.assertIn("location", activity)
            self.assertIn("trust_impact", activity)
            self.assertIn("details", activity)

    def test_get_sample_reviewer_activity_sorted(self) -> None:
        """Test that reviewer activity is sorted by date (descending)."""
        result = self.processor.get_sample_reviewer_activity()

        if len(result) > 1:
            # Check that dates are in descending order
            for i in range(len(result) - 1):
                self.assertGreaterEqual(result[i]["date"], result[i + 1]["date"])

    def test_generate_sample_reviews_default(self) -> None:
        """Test sample reviews generation with default count."""
        result = self.processor.generate_sample_reviews()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 20)  # Default count

        for review in result:
            self.assertIsInstance(review, dict)
            self.assertIn("text", review)
            self.assertIn("reviewer_data", review)
            self.assertIn("location_data", review)
            self.assertIn("timestamp", review)
            self.assertIn("rating", review)

            self.assertIn(review["rating"], [1, 2, 3, 4, 5])

    def test_generate_sample_reviews_custom_count(self) -> None:
        """Test sample reviews generation with custom count."""
        count = 5
        result = self.processor.generate_sample_reviews(count=count)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), count)

    def test_calculate_statistics_valid_data(self) -> None:
        """Test statistics calculation with valid data."""
        sample_data: list[Dict[str, Any]] = [
            {"trust_score": 0.8, "rating": 4},
            {"trust_score": 0.6, "rating": 3},
            {"trust_score": 0.9, "rating": 5},
            {"trust_score": 0.3, "rating": 2},
        ]

        result = self.processor.calculate_statistics(sample_data)

        self.assertIsInstance(result, dict)
        self.assertIn("total_reviews", result)
        self.assertIn("average_trust_score", result)
        self.assertIn("trust_score_std", result)
        self.assertIn("average_rating", result)
        self.assertIn("trust_distribution", result)
        self.assertIn("rating_distribution", result)

        self.assertEqual(result["total_reviews"], 4)
        self.assertGreaterEqual(result["average_trust_score"], 0.0)
        self.assertLessEqual(result["average_trust_score"], 1.0)

    def test_calculate_statistics_empty_data(self) -> None:
        """Test statistics calculation with empty data."""
        result = self.processor.calculate_statistics([])

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    def test_export_analysis_results_default_filename(self) -> None:
        """Test analysis results export with default filename."""
        sample_results: list[Dict[str, Any]] = [
            {"trust_score": 0.8, "text": "Great place!"},
            {"trust_score": 0.3, "text": "Terrible!"},
        ]

        result = self.processor.export_analysis_results(sample_results)

        self.assertIsInstance(result, dict)
        self.assertIn("timestamp", result)
        self.assertIn("summary", result)
        self.assertIn("detailed_results", result)
        self.assertIn("metadata", result)

        # Check summary
        summary = result["summary"]
        self.assertEqual(summary["total_analyzed"], 2)
        self.assertGreaterEqual(summary["average_trust_score"], 0.0)
        self.assertLessEqual(summary["average_trust_score"], 1.0)

    def test_export_analysis_results_custom_filename(self) -> None:
        """Test analysis results export with custom filename."""
        sample_results: list[Dict[str, Any]] = [{"trust_score": 0.8}]
        filename = "custom_export.json"

        result = self.processor.export_analysis_results(sample_results, filename)

        self.assertIsInstance(result, dict)
        self.assertIn("metadata", result)
        self.assertEqual(result["metadata"]["filename"], filename)

    def test_trend_data_date_format(self) -> None:
        """Test that trend data has proper date format."""
        result = self.processor.generate_trend_data(days=3)

        for trend in result:
            date_str = trend["date"]
            # Should be in YYYY-MM-DD format
            self.assertRegex(date_str, r"^\d{4}-\d{2}-\d{2}$")

    def test_reviewer_data_structure(self) -> None:
        """Test that generated reviewer data has proper structure."""
        result = self.processor.generate_sample_reviews(count=1)

        reviewer_data = result[0]["reviewer_data"]
        self.assertIn("id", reviewer_data)
        self.assertIn("account_age_days", reviewer_data)
        self.assertIn("review_count", reviewer_data)
        self.assertIn("profile_photo", reviewer_data)
        self.assertIn("verified_email", reviewer_data)
        self.assertIn("verified_phone", reviewer_data)
        self.assertIn("location_diversity", reviewer_data)

    def test_location_data_structure(self) -> None:
        """Test that generated location data has proper structure."""
        result = self.processor.generate_sample_reviews(count=1)

        location_data = result[0]["location_data"]
        self.assertIn("id", location_data)
        self.assertIn("name", location_data)
        self.assertIn("category", location_data)

    def test_consistency_across_calls(self) -> None:
        """Test that repeated calls maintain consistency in structure."""
        result1 = self.processor.generate_trend_data(days=5)
        result2 = self.processor.generate_trend_data(days=5)

        # Should have same structure
        self.assertEqual(len(result1), len(result2))
        self.assertEqual(set(result1[0].keys()), set(result2[0].keys()))


if __name__ == "__main__":
    unittest.main()
