"""
Unit tests for the FakeReviewDetector service.
"""

import unittest

from tests.test_config import (
    SAMPLE_REVIEWS,
    SAMPLE_REVIEWER_DATA,
    get_sample_trust_trends,
)
from backend.services.fake_detector import FakeReviewDetector


class TestFakeReviewDetector(unittest.TestCase):
    """Test cases for the FakeReviewDetector class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.detector = FakeReviewDetector()
        self.sample_review = SAMPLE_REVIEWS["positive"]

    def test_initialisation(self) -> None:
        """Test that FakeReviewDetector initialises correctly."""
        self.assertIsInstance(self.detector, FakeReviewDetector)
        self.assertIsInstance(self.detector.suspicious_patterns, list)
        self.assertIsInstance(self.detector.bot_indicators, list)
        self.assertGreater(len(self.detector.suspicious_patterns), 0)
        self.assertGreater(len(self.detector.bot_indicators), 0)

    def test_detect_fake_review_normal_text(self) -> None:
        """Test fake review detection with normal text."""
        result = self.detector.detect_fake_review(self.sample_review)

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_detect_fake_review_with_reviewer_data(self) -> None:
        """Test fake review detection with reviewer data."""
        trusted_data = SAMPLE_REVIEWER_DATA["trusted"]
        result = self.detector.detect_fake_review(self.sample_review, trusted_data)

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_detect_fake_review_suspicious_text(self) -> None:
        """Test fake review detection with suspicious text."""
        result = self.detector.detect_fake_review(SAMPLE_REVIEWS["suspicious"])

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        # Suspicious text should have higher fake probability
        self.assertGreater(result, 0.3)

    def test_detect_fake_review_fake_positive(self) -> None:
        """Test fake review detection with fake positive text."""
        result = self.detector.detect_fake_review(SAMPLE_REVIEWS["fake_positive"])

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        # Fake text should have higher fake probability
        self.assertGreater(result, 0.2)

    def test_detect_fake_review_empty_string(self) -> None:
        """Test fake review detection with empty string."""
        result = self.detector.detect_fake_review("")

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_trusted_vs_suspicious_reviewer(self) -> None:
        """Test that trusted reviewers get lower fake probability."""
        trusted_data = SAMPLE_REVIEWER_DATA["trusted"]
        suspicious_data = SAMPLE_REVIEWER_DATA["suspicious"]

        trusted_score = self.detector.detect_fake_review(
            self.sample_review, trusted_data
        )
        suspicious_score = self.detector.detect_fake_review(
            self.sample_review, suspicious_data
        )

        self.assertLess(trusted_score, suspicious_score)

    def test_detect_temporal_anomalies(self) -> None:
        """Test temporal anomaly detection."""
        trust_trends = get_sample_trust_trends(30)
        result = self.detector.detect_temporal_anomalies(trust_trends)

        self.assertIsInstance(result, list)
        for anomaly in result:
            self.assertIsInstance(anomaly, dict)
            self.assertIn("timestamp", anomaly)
            self.assertIn("anomaly_type", anomaly)

    def test_detect_temporal_anomalies_insufficient_data(self) -> None:
        """Test temporal anomaly detection with insufficient data."""
        trust_trends = get_sample_trust_trends(5)  # Less than minimum required
        result = self.detector.detect_temporal_anomalies(trust_trends)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_get_risk_factors(self) -> None:
        """Test risk factors extraction."""
        result = self.detector.get_risk_factors(self.sample_review)

        self.assertIsInstance(result, dict)
        self.assertIn("text_suspicion", result)
        self.assertIn("behavior_suspicion", result)
        self.assertIn("network_suspicion", result)
        self.assertIn("overall_risk", result)

        for factor in result.values():
            if isinstance(factor, (int, float)):
                self.assertGreaterEqual(factor, 0.0)
                self.assertLessEqual(factor, 1.0)

    def test_get_risk_factors_with_reviewer_data(self) -> None:
        """Test risk factors extraction with reviewer data."""
        result = self.detector.get_risk_factors(
            self.sample_review, SAMPLE_REVIEWER_DATA["suspicious"]
        )

        self.assertIsInstance(result, dict)
        self.assertIn("behavior_suspicion", result)
        # Should have higher behavior suspicion with suspicious reviewer
        self.assertGreater(result["behavior_suspicion"], 0.3)

    def test_multiple_detections_consistency(self) -> None:
        """Test that multiple detections on same text are consistent."""
        result1 = self.detector.detect_fake_review(self.sample_review)
        result2 = self.detector.detect_fake_review(self.sample_review)

        # Results should be identical for same input
        self.assertEqual(result1, result2)

    def test_different_texts_different_scores(self) -> None:
        """Test that different texts produce different fake scores."""
        normal_score = self.detector.detect_fake_review(SAMPLE_REVIEWS["positive"])
        suspicious_score = self.detector.detect_fake_review(
            SAMPLE_REVIEWS["suspicious"]
        )

        # Scores should be different
        self.assertNotEqual(normal_score, suspicious_score)
        self.assertGreater(suspicious_score, normal_score)

    def test_error_handling_none_input(self) -> None:
        """Test error handling with None input."""
        with self.assertRaises(Exception):
            self.detector.detect_fake_review(None)  # type: ignore

    def test_error_handling_non_string_input(self) -> None:
        """Test error handling with non-string input."""
        with self.assertRaises(Exception):
            self.detector.detect_fake_review(123)  # type: ignore

    def test_text_pattern_analysis(self) -> None:
        """Test text pattern analysis (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.detector._analyze_text_patterns(self.sample_review)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_reviewer_behavior_analysis(self) -> None:
        """Test reviewer behavior analysis (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.detector._analyze_reviewer_behavior(SAMPLE_REVIEWER_DATA["trusted"])  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_network_analysis(self) -> None:
        """Test network analysis (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.detector._simple_network_analysis(SAMPLE_REVIEWER_DATA["trusted"])  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
