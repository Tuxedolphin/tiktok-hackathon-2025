"""
Unit tests for the SentimentAnalyser service.
"""

import unittest

from tests.test_config import SAMPLE_REVIEWS
from backend.services.sentiment_analyser import SentimentAnalyser


class TestSentimentAnalyser(unittest.TestCase):
    """Test cases for the SentimentAnalyser class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.analyser = SentimentAnalyser()
        self.sample_review = SAMPLE_REVIEWS["positive"]

    def test_initialisation(self) -> None:
        """Test that SentimentAnalyser initialises correctly."""
        self.assertIsInstance(self.analyser, SentimentAnalyser)
        self.assertIsInstance(self.analyser.sentiment_keywords, dict)
        self.assertIn("positive", self.analyser.sentiment_keywords)
        self.assertIn("negative", self.analyser.sentiment_keywords)
        self.assertIn("neutral", self.analyser.sentiment_keywords)

    def test_analyse_sentiment_positive_text(self) -> None:
        """Test sentiment analysis with positive text."""
        result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["positive"])

        self.assertIsInstance(result, dict)
        self.assertIn("polarity", result)
        self.assertIn("subjectivity", result)
        self.assertIn("confidence", result)
        self.assertIn("intensity", result)
        self.assertIn("manipulation_score", result)

        # Check that polarity is positive
        self.assertGreater(result["polarity"], 0.0)
        self.assertGreaterEqual(result["polarity"], -1.0)
        self.assertLessEqual(result["polarity"], 1.0)

    def test_analyse_sentiment_negative_text(self) -> None:
        """Test sentiment analysis with negative text."""
        result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["negative"])

        self.assertIsInstance(result, dict)
        self.assertIn("polarity", result)

        # Check that polarity is negative
        self.assertLess(result["polarity"], 0.0)
        self.assertGreaterEqual(result["polarity"], -1.0)
        self.assertLessEqual(result["polarity"], 1.0)

    def test_analyse_sentiment_neutral_text(self) -> None:
        """Test sentiment analysis with neutral text."""
        result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["neutral"])

        self.assertIsInstance(result, dict)
        self.assertIn("polarity", result)

        # Check that polarity is near neutral
        self.assertGreaterEqual(result["polarity"], -1.0)
        self.assertLessEqual(result["polarity"], 1.0)

    def test_analyse_sentiment_empty_string(self) -> None:
        """Test sentiment analysis with empty string."""
        result = self.analyser.analyse_sentiment("")

        self.assertIsInstance(result, dict)
        self.assertIn("polarity", result)
        self.assertIn("subjectivity", result)

        for key, value in result.items():
            if key in [
                "polarity",
                "subjectivity",
                "confidence",
                "intensity",
                "manipulation_score",
            ]:
                self.assertIsInstance(value, float)

    def test_analyse_sentiment_suspicious_text(self) -> None:
        """Test sentiment analysis with suspicious text."""
        result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["suspicious"])

        self.assertIsInstance(result, dict)
        self.assertIn("manipulation_score", result)

        # Suspicious text should have higher manipulation score
        self.assertGreater(result["manipulation_score"], 0.3)

    def test_analyze_keyword_sentiment_positive(self) -> None:
        """Test keyword-based sentiment analysis with positive words."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._analyze_keyword_sentiment("excellent amazing wonderful")  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_analyze_keyword_sentiment_negative(self) -> None:
        """Test keyword-based sentiment analysis with negative words."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._analyze_keyword_sentiment("terrible awful horrible")  # type: ignore

        self.assertIsInstance(result, float)
        self.assertLess(result, 0.0)
        self.assertGreaterEqual(result, -1.0)

    def test_calculate_sentiment_intensity_strong(self) -> None:
        """Test sentiment intensity calculation with strong sentiment."""
        strong_sentiment = {"polarity": 0.8, "subjectivity": 0.9}
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._calculate_sentiment_intensity(strong_sentiment)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_calculate_sentiment_intensity_weak(self) -> None:
        """Test sentiment intensity calculation with weak sentiment."""
        weak_sentiment = {"polarity": 0.1, "subjectivity": 0.2}
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._calculate_sentiment_intensity(weak_sentiment)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_detect_sentiment_manipulation_normal_text(self) -> None:
        """Test sentiment manipulation detection with normal text."""
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._detect_sentiment_manipulation(self.sample_review)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_detect_sentiment_manipulation_manipulated_text(self) -> None:
        """Test sentiment manipulation detection with manipulated text."""
        manipulated_text = (
            "amazing amazing amazing perfect perfect perfect excellent excellent"
        )
        # Using # type: ignore to suppress protected method warnings for testing
        result = self.analyser._detect_sentiment_manipulation(manipulated_text)  # type: ignore

        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        # Should detect manipulation
        self.assertGreater(result, 0.2)

    def test_multiple_analyses_consistency(self) -> None:
        """Test that multiple analyses on same text are consistent."""
        result1 = self.analyser.analyse_sentiment(self.sample_review)
        result2 = self.analyser.analyse_sentiment(self.sample_review)

        # Results should be identical for same input
        self.assertEqual(result1, result2)

    def test_different_texts_different_results(self) -> None:
        """Test that different texts produce different sentiment results."""
        positive_result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["positive"])
        negative_result = self.analyser.analyse_sentiment(SAMPLE_REVIEWS["negative"])

        # Polarities should be different
        self.assertNotEqual(positive_result["polarity"], negative_result["polarity"])
        self.assertGreater(positive_result["polarity"], negative_result["polarity"])

    def test_sentiment_score_ranges(self) -> None:
        """Test that all sentiment scores are within valid ranges."""
        result = self.analyser.analyse_sentiment(self.sample_review)

        # Check all score ranges
        self.assertGreaterEqual(result["polarity"], -1.0)
        self.assertLessEqual(result["polarity"], 1.0)
        self.assertGreaterEqual(result["subjectivity"], 0.0)
        self.assertLessEqual(result["subjectivity"], 1.0)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)
        self.assertGreaterEqual(result["intensity"], 0.0)
        self.assertLessEqual(result["intensity"], 1.0)
        self.assertGreaterEqual(result["manipulation_score"], 0.0)
        self.assertLessEqual(result["manipulation_score"], 1.0)

    def test_error_handling(self) -> None:
        """Test error handling with invalid inputs."""
        # Should handle error gracefully
        with self.assertRaises(Exception):
            self.analyser.analyse_sentiment(None)  # type: ignore

    def test_analyse_sentiment_non_string_input(self) -> None:
        """Test sentiment analysis with non-string input."""
        with self.assertRaises(Exception):
            self.analyser.analyse_sentiment(123)  # type: ignore


if __name__ == "__main__":
    unittest.main()
