"""
Unit tests for the TrustScorer service.
"""

import unittest

from tests.test_config import SAMPLE_REVIEWS, SAMPLE_REVIEWER_DATA, SAMPLE_LOCATION_DATA
from backend.services.trust_scorer import TrustScorer


class TestTrustScorer(unittest.TestCase):
    """Test cases for the TrustScorer class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.scorer = TrustScorer()
        self.sample_review = SAMPLE_REVIEWS["positive"]
        self.sample_sentiment = {
            "polarity": 0.5,
            "subjectivity": 0.6,
            "confidence": 0.8,
        }

    def test_initialisation(self) -> None:
        """Test that TrustScorer initialises correctly."""
        self.assertIsInstance(self.scorer, TrustScorer)
        self.assertIsInstance(self.scorer.weights, dict)
        self.assertIn("authenticity", self.scorer.weights)
        self.assertIn("sentiment_quality", self.scorer.weights)
        self.assertIn("reviewer_credibility", self.scorer.weights)

    def test_calculate_trust_score_basic(self) -> None:
        """Test basic trust score calculation."""
        result = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.8,  # authenticity_score
            0.2,  # fake_probability
        )

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_trust_score_with_reviewer_data(self) -> None:
        """Test trust score calculation with reviewer data."""
        result = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.8,
            0.2,
            SAMPLE_REVIEWER_DATA["trusted"],
        )

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_trust_score_with_location_data(self) -> None:
        """Test trust score calculation with location data."""
        result = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.8,
            0.2,
            SAMPLE_REVIEWER_DATA["trusted"],
            SAMPLE_LOCATION_DATA["restaurant"],
        )

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_trusted_vs_suspicious_reviewer(self) -> None:
        """Test that trusted reviewers get higher trust scores."""
        trusted_score = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.7,
            0.3,
            SAMPLE_REVIEWER_DATA["trusted"],
        )

        suspicious_score = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.7,
            0.3,
            SAMPLE_REVIEWER_DATA["suspicious"],
        )

        self.assertGreater(trusted_score, suspicious_score)

    def test_high_vs_low_authenticity(self) -> None:
        """Test that higher authenticity scores lead to higher trust scores."""
        high_auth_score = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.9,  # high authenticity
            0.1,  # low fake probability
        )

        low_auth_score = self.scorer.calculate_trust_score(
            self.sample_review,
            self.sample_sentiment,
            0.3,  # low authenticity
            0.7,  # high fake probability
        )

        self.assertGreater(high_auth_score, low_auth_score)

    def test_get_trust_category(self) -> None:
        """Test trust score categorisation."""
        # Test different score ranges
        high_score = 0.9
        medium_score = 0.5
        low_score = 0.1

        self.assertEqual(self.scorer.get_trust_category(high_score), "highly_trusted")
        self.assertEqual(self.scorer.get_trust_category(medium_score), "moderate")
        self.assertEqual(self.scorer.get_trust_category(low_score), "untrusted")

    def test_get_trust_explanation(self) -> None:
        """Test trust score explanation generation."""
        components = {
            "authenticity_score": 0.8,
            "fake_probability": 0.2,
            "reviewer_credibility": 0.7,
        }

        explanation = self.scorer.get_trust_explanation(0.8, components)

        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)

    def test_get_trust_explanation_low_score(self) -> None:
        """Test trust explanation for low trust scores."""
        components = {
            "authenticity_score": 0.2,
            "fake_probability": 0.8,
            "reviewer_credibility": 0.2,
        }

        explanation = self.scorer.get_trust_explanation(0.2, components)

        self.assertIsInstance(explanation, str)
        self.assertIn("concerns", explanation.lower())

    def test_calculate_location_trust(self) -> None:
        """Test location trust calculation."""
        sample_results = [
            {"trust_score": 0.8, "success": True},
            {"trust_score": 0.7, "success": True},
            {"trust_score": 0.9, "success": True},
            {"trust_score": 0.6, "success": True},
        ]

        result = self.scorer.calculate_location_trust(sample_results)

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_location_trust_empty_results(self) -> None:
        """Test location trust calculation with empty results."""
        result = self.scorer.calculate_location_trust([])

        self.assertEqual(result, 0.5)  # Default value

    def test_calculate_location_trust_failed_results(self) -> None:
        """Test location trust calculation with failed results."""
        failed_results = [
            {"trust_score": 0.8, "success": False},
            {"trust_score": 0.7, "success": False},
        ]

        result = self.scorer.calculate_location_trust(failed_results)

        self.assertEqual(result, 0.5)  # Default when no successful results

    def test_score_consistency(self) -> None:
        """Test that multiple calculations are consistent."""
        score1 = self.scorer.calculate_trust_score(
            self.sample_review, self.sample_sentiment, 0.8, 0.2
        )

        score2 = self.scorer.calculate_trust_score(
            self.sample_review, self.sample_sentiment, 0.8, 0.2
        )

        self.assertEqual(score1, score2)

    def test_score_bounds(self) -> None:
        """Test that trust scores stay within bounds."""
        # Test extreme values
        extreme_high = self.scorer.calculate_trust_score(
            self.sample_review,
            {"polarity": 1.0, "subjectivity": 0.0, "confidence": 1.0},
            1.0,  # perfect authenticity
            0.0,  # no fake probability
        )

        extreme_low = self.scorer.calculate_trust_score(
            self.sample_review,
            {"polarity": -1.0, "subjectivity": 1.0, "confidence": 0.0},
            0.0,  # no authenticity
            1.0,  # completely fake
        )

        self.assertGreaterEqual(extreme_high, 0.0)
        self.assertLessEqual(extreme_high, 1.0)
        self.assertGreaterEqual(extreme_low, 0.0)
        self.assertLessEqual(extreme_low, 1.0)

    def test_error_handling(self) -> None:
        """Test error handling with invalid inputs."""
        # Should handle errors gracefully
        result = self.scorer.calculate_trust_score(
            None, self.sample_sentiment, 0.8, 0.2  # type: ignore
        )

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_sentiment_quality_assessment(self) -> None:
        """Test sentiment quality assessment (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.scorer._assess_sentiment_quality(self.sample_sentiment)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_content_quality_assessment(self) -> None:
        """Test content quality assessment (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.scorer._assess_content_quality(self.sample_review)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_reviewer_credibility_calculation(self) -> None:
        """Test reviewer credibility calculation (protected method)."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.scorer._calculate_reviewer_credibility(SAMPLE_REVIEWER_DATA["trusted"])  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
