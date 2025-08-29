"""
ML services for review trust analysis.

Contains the core machine learning algorithms for:
- Review authenticity analysis
- Sentiment analysis and manipulation detection
- Fake review detection
- Trust scoring

Exports use British English class names by default, with backwards-compatible
aliases for the original American spellings.
"""

from .review_analyser import ReviewAnalyser
from .sentiment_analyser import SentimentAnalyser
from .fake_detector import FakeReviewDetector
from .trust_scorer import TrustScorer

# Backwards-compatible aliases (American spelling)
ReviewAnalyzer = ReviewAnalyser  # type: ignore
SentimentAnalyzer = SentimentAnalyser  # type: ignore

__all__ = [
    "ReviewAnalyser",
    "SentimentAnalyser",
    "FakeReviewDetector",
    "TrustScorer",
    # Aliases
    "ReviewAnalyzer",
    "SentimentAnalyzer",
]
