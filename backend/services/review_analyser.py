import numpy as np  # type: ignore
import re
from textblob import TextBlob  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from typing import Dict, Optional, Any, List


class ReviewAnalyser:
    """
    Review Analyser - Determines review authenticity using linguistic analysis.

    Analyses review authenticity using multiple linguistic and behavioural features.
    Uses natural language processing to detect patterns that indicate genuine vs fake reviews.
    """

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        self.common_fake_patterns = [
            r"\b(amazing|perfect|excellent|outstanding)\b.*\b(amazing|perfect|excellent|outstanding)\b",
            r"\b(worst|terrible|awful|horrible)\b.*\b(worst|terrible|awful|horrible)\b",
            r"([!]{2,})",
            r"(\b\w+\b)(\s+\1\b){2,}",  # Repeated words
        ]

    def calculate_authenticity(
        self, review_text: Any, reviewer_data: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate overall authenticity score for a review
        """
        # Validate inputs
        if not isinstance(review_text, str):
            raise TypeError("review_text must be a string")

        try:
            # Text-based features
            linguistic_score = self._analyse_linguistic_features(review_text)
            sentiment_consistency = self._check_sentiment_consistency(review_text)

            # Reviewer-based features (if available)
            reviewer_score = 1.0
            if reviewer_data:
                reviewer_score = self._analyse_reviewer_behaviour(reviewer_data)

            # Combine scores with weights
            authenticity_score = (
                linguistic_score * 0.4
                + sentiment_consistency * 0.3
                + reviewer_score * 0.3
            )

            return max(0.0, min(1.0, authenticity_score))

        except Exception as e:
            print(f"Error calculating authenticity: {e}")
            return 0.5  # Default neutral score

    def _analyse_linguistic_features(self, text: str) -> float:
        """
        Analyse linguistic patterns that indicate authenticity.

        Examines writing quality, sentiment consistency, and linguistic sophistication
        to determine if the review text appears genuine.
        """
        if not text or len(text.strip()) < 10:
            return 0.3

        score = 1.0

        # Check for fake patterns
        fake_pattern_count = 0
        for pattern in self.common_fake_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                fake_pattern_count += 1

        score -= fake_pattern_count * 0.2

        # Length analysis (too short or too long can be suspicious)
        word_count = len(text.split())
        if word_count < 5:
            score -= 0.3
        elif word_count > 500:
            score -= 0.2

        # Spelling and grammar quality
        blob = TextBlob(text)
        try:
            corrected = str(blob.correct())
            error_ratio = len(
                [
                    i
                    for i in range(len(text))
                    if i < len(corrected) and text[i] != corrected[i]
                ]
            ) / len(text)
            if error_ratio > 0.1:
                score -= 0.2
        except:
            pass

        # Readability (simple heuristic)
        sentences = text.split(".")
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        if avg_sentence_length < 3 or avg_sentence_length > 40:
            score -= 0.1

        return max(0.0, min(1.0, score))

    def _check_sentiment_consistency(self, text: str) -> float:
        """
        Check if sentiment is consistent throughout the review
        """
        try:
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            if len(sentences) < 2:
                return 1.0

            sentiments: List[float] = []
            for sentence in sentences:
                blob = TextBlob(sentence)
                sentiment_polarity = float(blob.sentiment.polarity)  # type: ignore
                sentiments.append(sentiment_polarity)

            # Calculate consistency (lower variance = more consistent)
            variance = float(np.var(sentiments))
            consistency_score = max(0.0, 1.0 - variance)

            return consistency_score

        except Exception:
            return 0.7  # Default moderate score

    def _analyse_reviewer_behaviour(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Analyse reviewer behavioural patterns.

        Examines account age, review frequency, and other behavioural indicators
        to assess reviewer credibility.
        """
        try:
            score = 1.0

            # Account age factor
            account_age = reviewer_data.get("account_age_days", 0)
            if account_age < 30:
                score -= 0.3
            elif account_age < 90:
                score -= 0.1

            # Review frequency
            review_count = reviewer_data.get("review_count", 0)
            if review_count == 0:
                score -= 0.4
            elif review_count < 5:
                score -= 0.2
            elif review_count > 1000:
                score -= 0.1  # Suspiciously high

            # Profile completeness
            if not reviewer_data.get("profile_photo", False):
                score -= 0.1
            if not reviewer_data.get("verified_email", False):
                score -= 0.1

            return max(0.0, min(1.0, score))

        except Exception:
            return 0.7

    def get_authenticity_factors(self, text: str) -> Dict[str, float]:
        """
        Get detailed breakdown of authenticity factors
        """
        linguistic = self._analyse_linguistic_features(text)
        sentiment_consistency = self._check_sentiment_consistency(text)
        length_score = self._check_length_appropriateness(text)
        spam_score = self._detect_spam_indicators(text)

        # Provide both British, descriptive keys and the test-expected keys
        factors = {
            # Expected by tests
            "linguistic_score": linguistic,
            "length_score": length_score,
            "spam_score": spam_score,
            # Additional rich factors
            "linguistic_quality": linguistic,
            "sentiment_consistency": sentiment_consistency,
            "length_appropriate": length_score,
            "spam_indicators": spam_score,
        }

        return factors

    def _check_length_appropriateness(self, text: str) -> float:
        """
        Check if review length is appropriate
        """
        word_count = len(text.split())
        if 10 <= word_count <= 200:
            return 1.0
        elif 5 <= word_count <= 300:
            return 0.8
        else:
            return 0.3

    def _detect_spam_indicators(self, text: str) -> float:
        """
        Detect common spam indicators
        """
        spam_score = 0.0

        # Excessive capitalization
        if len(re.findall(r"[A-Z]", text)) / len(text) > 0.3:
            spam_score += 0.3

        # Excessive punctuation
        if len(re.findall(r"[!?]", text)) / len(text) > 0.1:
            spam_score += 0.2

        # Promotional keywords
        promo_keywords = [
            "discount",
            "coupon",
            "deal",
            "offer",
            "sale",
            "cheap",
            "free",
        ]
        promo_count = sum(
            1 for keyword in promo_keywords if keyword.lower() in text.lower()
        )
        spam_score += min(0.3, promo_count * 0.1)

        return max(0.0, 1.0 - spam_score)
