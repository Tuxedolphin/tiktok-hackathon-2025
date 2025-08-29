"""
Tests for backend.services exports and compatibility aliases.
"""

import unittest


class TestServicesExports(unittest.TestCase):
    def test_exports_british_and_american_aliases(self) -> None:
        from backend import services

        # British spellings
        self.assertTrue(hasattr(services, "ReviewAnalyser"))
        self.assertTrue(hasattr(services, "SentimentAnalyser"))

        # American aliases
        self.assertTrue(hasattr(services, "ReviewAnalyzer"))
        self.assertTrue(hasattr(services, "SentimentAnalyzer"))

        # __all__ includes both
        self.assertIn("ReviewAnalyser", services.__all__)
        self.assertIn("SentimentAnalyser", services.__all__)
        self.assertIn("ReviewAnalyzer", services.__all__)
        self.assertIn("SentimentAnalyzer", services.__all__)

    def test_can_instantiate_all_services(self) -> None:
        from backend.services import (
            ReviewAnalyser,
            ReviewAnalyzer,
            SentimentAnalyser,
            SentimentAnalyzer,
            FakeReviewDetector,
            TrustScorer,
        )

        # Instances should construct without error
        self.assertIsNotNone(ReviewAnalyser())
        self.assertIsNotNone(ReviewAnalyzer())
        self.assertIsNotNone(SentimentAnalyser())
        self.assertIsNotNone(SentimentAnalyzer())
        self.assertIsNotNone(FakeReviewDetector())
        self.assertIsNotNone(TrustScorer())
