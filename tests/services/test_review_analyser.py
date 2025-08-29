"""
Unit tests for the ReviewAnalyser service.
"""

import unittest
from unittest.mock import patch

from tests.test_config import SAMPLE_REVIEWS, SAMPLE_REVIEWER_DATA
from backend.services.review_analyser import ReviewAnalyser


class TestReviewAnalyser(unittest.TestCase):
    """Test cases for the ReviewAnalyser class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.analyser = ReviewAnalyser()
        self.sample_review = SAMPLE_REVIEWS["positive"]

    def test_initialisation(self) -> None:
        """Test that ReviewAnalyser initialises correctly."""
        self.assertIsInstance(self.analyser, ReviewAnalyser)
        self.assertIsInstance(self.analyser.vectorizer, object)
        self.assertIsInstance(self.analyser.common_fake_patterns, list)
        self.assertGreater(len(self.analyser.common_fake_patterns), 0)

    def test_calculate_authenticity_valid_input(self) -> None:
        """Test authenticity calculation with valid input."""
        result = self.analyser.calculate_authenticity(self.sample_review)

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_with_reviewer_data(self) -> None:
        """Test authenticity calculation with reviewer data."""
        reviewer_data = SAMPLE_REVIEWER_DATA["trusted"]
        result = self.analyser.calculate_authenticity(self.sample_review, reviewer_data)

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_empty_string(self) -> None:
        """Test authenticity calculation with empty string."""
        result = self.analyser.calculate_authenticity("")

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_short_text(self) -> None:
        """Test authenticity calculation with very short text."""
        result = self.analyser.calculate_authenticity("Good")

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_long_text(self) -> None:
        """Test authenticity calculation with long text."""
        result = self.analyser.calculate_authenticity(SAMPLE_REVIEWS["long"])

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_suspicious_text(self) -> None:
        """Test authenticity calculation with suspicious text."""
        result = self.analyser.calculate_authenticity(SAMPLE_REVIEWS["suspicious"])

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        # Suspicious text should have lower authenticity
        self.assertLess(result, 0.8)

    def test_get_authenticity_factors(self) -> None:
        """Test authenticity factors extraction."""
        result = self.analyser.get_authenticity_factors(self.sample_review)

        self.assertIsInstance(result, dict)
        self.assertIn("linguistic_score", result)
        self.assertIn("sentiment_consistency", result)
        self.assertIn("length_score", result)
        self.assertIn("spam_score", result)

        for score in result.values():
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_multiple_calculations_consistency(self) -> None:
        """Test that multiple calculations on same text are consistent."""
        result1 = self.analyser.calculate_authenticity(self.sample_review)
        result2 = self.analyser.calculate_authenticity(self.sample_review)

        # Results should be identical for same input
        self.assertEqual(result1, result2)

    def test_different_reviews_different_scores(self) -> None:
        """Test that different reviews produce different scores."""
        score1 = self.analyser.calculate_authenticity(SAMPLE_REVIEWS["positive"])
        score2 = self.analyser.calculate_authenticity(SAMPLE_REVIEWS["negative"])
        score3 = self.analyser.calculate_authenticity(SAMPLE_REVIEWS["suspicious"])

        # Scores should be different (with high probability)
        scores = [score1, score2, score3]
        unique_scores = set(scores)
        self.assertGreater(
            len(unique_scores), 1, "Different reviews should produce different scores"
        )

    def test_trusted_vs_suspicious_reviewer(self) -> None:
        """Test that trusted reviewers get higher authenticity scores."""
        trusted_data = SAMPLE_REVIEWER_DATA["trusted"]
        suspicious_data = SAMPLE_REVIEWER_DATA["suspicious"]

        trusted_score = self.analyser.calculate_authenticity(
            self.sample_review, trusted_data
        )
        suspicious_score = self.analyser.calculate_authenticity(
            self.sample_review, suspicious_data
        )

        self.assertGreater(trusted_score, suspicious_score)

    def test_error_handling(self) -> None:
        """Test error handling with invalid inputs."""
        # Should handle error gracefully and return a default value
        with patch.object(
            self.analyser,
            "_analyse_linguistic_features",
            side_effect=Exception("Test error"),
        ):
            result = self.analyser.calculate_authenticity(self.sample_review)
            self.assertIsInstance(result, float)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)

    def test_calculate_authenticity_none_input(self) -> None:
        """Test authenticity calculation with None input."""
        with self.assertRaises(Exception):
            self.analyser.calculate_authenticity(None)  # type: ignore

    def test_calculate_authenticity_non_string_input(self) -> None:
        """Test authenticity calculation with non-string input."""
        with self.assertRaises(Exception):
            self.analyser.calculate_authenticity(123)  # type: ignore

    # Test a few protected methods that are critical
    def test_linguistic_features_analysis(self) -> None:
        """Test linguistic features analysis (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._analyse_linguistic_features(self.sample_review)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_reviewer_behaviour_analysis(self) -> None:
        """Test reviewer behaviour analysis (protected method)."""
        trusted_data = SAMPLE_REVIEWER_DATA["trusted"]
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._analyse_reviewer_behaviour(trusted_data)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
