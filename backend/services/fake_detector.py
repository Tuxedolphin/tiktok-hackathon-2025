import numpy as np  # type: ignore
import re
from typing import Dict, List, Optional, Any


class FakeReviewDetector:
    """
    Detects fake reviews using ML techniques and pattern analysis
    """

    def __init__(self):
        self.suspicious_patterns = [
            r"\b(buy|purchase|order)\b.*\b(recommend|suggest)\b",  # Commercial language
            r"\b(friends?|family)\b.*\b(love|recommend)\b",  # Fake social proof
            r"\b(five|5)\s*star",  # Explicit rating mentions
            r"\b(must try|must visit|must have)\b",  # Pressure language
        ]

        self.bot_indicators = [
            r"^.{1,20}$",  # Very short reviews
            r"(.)\1{3,}",  # Repeated characters
            r"\b(\w+)\s+\1\b",  # Repeated words
        ]

    def detect_fake_review(
        self, review_text: Any, reviewer_data: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate probability that a review is fake (0-1 scale)
        """
        if not isinstance(review_text, str):
            # Let invalid input raise for tests that expect exceptions
            raise TypeError("review_text must be a string")
        try:
            # Text-based analysis
            text_suspicion = self._analyze_text_patterns(review_text)

            # Reviewer behavioral analysis
            behavior_suspicion = 0.0
            if reviewer_data:
                behavior_suspicion = self._analyze_reviewer_behavior(reviewer_data)

            # Network analysis (simplified)
            network_suspicion = (
                self._simple_network_analysis(reviewer_data) if reviewer_data else 0.0
            )

            # Combine suspicion scores
            if reviewer_data:
                combined_suspicion = (
                    text_suspicion * 0.45
                    + behavior_suspicion * 0.35
                    + network_suspicion * 0.2
                )
            else:
                # When no reviewer context, lean more on text evidence
                combined_suspicion = text_suspicion * 0.8 + network_suspicion * 0.2

            return min(1.0, max(0.0, combined_suspicion))

        except Exception as e:
            print(f"Error detecting fake review: {e}")
            return 0.5  # Default uncertain score

    def _analyze_text_patterns(self, text: str) -> float:
        """
        Analyze text patterns for fake review indicators
        """
        if not text:
            return 0.8  # Empty text is suspicious

        suspicion_score = 0.0

        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                suspicion_score += 0.2

        # Check for bot-like patterns
        for pattern in self.bot_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                suspicion_score += 0.25

        # Length analysis
        word_count = len(text.split())
        if word_count < 3:
            suspicion_score += 0.35
        elif word_count > 500:
            suspicion_score += 0.1

        # Generic language detection
        generic_phrases = [
            "good service",
            "nice place",
            "friendly staff",
            "great food",
            "bad experience",
            "poor service",
            "would not recommend",
        ]

        generic_count = sum(
            1 for phrase in generic_phrases if phrase.lower() in text.lower()
        )
        if generic_count > 2:
            suspicion_score += 0.25

        # Check for emotional manipulation
        emotional_words = [
            "amazing",
            "terrible",
            "perfect",
            "worst",
            "best",
            "horrible",
        ]
        emotional_density = sum(
            1 for word in emotional_words if word.lower() in text.lower()
        ) / len(text.split())
        if emotional_density > 0.15:
            suspicion_score += 0.25

        # Repeated sentiment words (e.g., "amazing amazing amazing")
        if re.search(r"\b(\w+)\b(?:\s+\1\b){1,}", text, re.IGNORECASE):
            suspicion_score += 0.2

        return min(1.0, suspicion_score)

    def _analyze_reviewer_behavior(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Analyze reviewer behavior patterns for suspicious activity
        """
        suspicion_score = 0.0

        # New account with many reviews
        account_age = reviewer_data.get("account_age_days", 365)
        review_count = reviewer_data.get("review_count", 0)

        # Very new accounts are inherently riskier
        if account_age < 30:
            suspicion_score += 0.1
        if account_age < 30 and review_count > 20:
            suspicion_score += 0.4
        elif account_age < 90 and review_count > 50:
            suspicion_score += 0.3

        # Review frequency analysis
        if review_count > 0 and account_age > 0:
            reviews_per_day = review_count / account_age
            if reviews_per_day > 2:  # More than 2 reviews per day average
                suspicion_score += 0.3

        # Profile completeness (incomplete profiles are suspicious)
        profile_score = 0
        if reviewer_data.get("profile_photo", False):
            profile_score += 1
        if reviewer_data.get("verified_email", False):
            profile_score += 1
        if reviewer_data.get("verified_phone", False):
            profile_score += 1

        if profile_score == 0:
            suspicion_score += 0.3
        elif profile_score == 1:
            suspicion_score += 0.1

        # Review pattern analysis
        recent_reviews = reviewer_data.get("recent_reviews", [])
        if len(recent_reviews) > 5:
            # Check for same-day multiple reviews
            same_day_reviews = self._count_same_day_reviews(recent_reviews)
            if same_day_reviews > 3:
                suspicion_score += 0.2

        return min(1.0, suspicion_score)

    def _simple_network_analysis(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Simple network analysis for coordinated behavior
        """
        suspicion_score = 0.0

        # Check for suspicious reviewer connections (simplified)
        similar_reviewers = reviewer_data.get("similar_reviewers", [])
        if len(similar_reviewers) > 10:
            suspicion_score += 0.3

        # IP-based clustering (simplified)
        ip_cluster_size = reviewer_data.get("ip_cluster_size", 1)
        if ip_cluster_size > 5:
            suspicion_score += 0.4

        return min(1.0, suspicion_score)

    def _count_same_day_reviews(self, reviews: List[Dict[str, Any]]) -> int:
        """
        Count reviews posted on the same day.

        Args:
            reviews: List of review dictionaries

        Returns:
            Maximum number of reviews posted on any single day
        """
        try:
            dates = [review.get("date", "") for review in reviews if review.get("date")]
            date_counts: Dict[str, int] = {}

            for date_str in dates:
                date_only = date_str.split(" ")[0]  # Get just the date part
                date_counts[date_only] = date_counts.get(date_only, 0) + 1

            return max(date_counts.values()) if date_counts else 0
        except:
            return 0

    def detect_temporal_anomalies(
        self, trust_trends: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect temporal anomalies in review patterns.

        Args:
            trust_trends: List of dictionaries containing trust trend data

        Returns:
            List of detected anomalies with details
        """
        try:
            if len(trust_trends) < 10:
                return []

            # Extract trust scores and timestamps
            scores = [trend["trust_score"] for trend in trust_trends]
            timestamps = [trend["timestamp"] for trend in trust_trends]

            # Simple anomaly detection using z-score
            mean_score = float(np.mean(scores))
            std_score = float(np.std(scores))

            anomalies: List[Dict[str, Any]] = []
            for score, timestamp in zip(scores, timestamps):
                if std_score > 0:
                    z_score = abs(score - mean_score) / std_score
                    if z_score > 2:  # Anomaly threshold
                        anomalies.append(
                            {
                                "timestamp": timestamp,
                                "trust_score": score,
                                "anomaly_type": "score_outlier",
                                "severity": min(1.0, z_score / 3),
                            }
                        )

            # Detect review bombing patterns
            bombing_anomalies = self._detect_review_bombing(trust_trends)
            anomalies.extend(bombing_anomalies)

            return anomalies

        except Exception as e:
            print(f"Error detecting temporal anomalies: {e}")
            return []

    def _detect_review_bombing(
        self, trust_trends: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect review bombing patterns.

        Args:
            trust_trends: List of trust trend data

        Returns:
            List of detected review bombing anomalies
        """
        anomalies: List[Dict[str, Any]] = []

        try:
            # Group reviews by day
            daily_reviews: Dict[str, List[Dict[str, Any]]] = {}
            for trend in trust_trends:
                timestamp = trend["timestamp"]
                date_key = (
                    timestamp.split("T")[0]
                    if "T" in timestamp
                    else timestamp.split(" ")[0]
                )

                if date_key not in daily_reviews:
                    daily_reviews[date_key] = []
                daily_reviews[date_key].append(trend)

            # Check for unusual daily volumes
            daily_counts = [len(reviews) for reviews in daily_reviews.values()]
            if daily_counts:
                mean_daily = float(np.mean(daily_counts))

                for date, reviews in daily_reviews.items():
                    if len(reviews) > mean_daily * 3:  # 3x normal volume
                        trust_scores = [r["trust_score"] for r in reviews]
                        avg_trust = float(np.mean(trust_scores))

                        anomalies.append(
                            {
                                "timestamp": date,
                                "trust_score": avg_trust,
                                "anomaly_type": "review_bombing",
                                "severity": min(
                                    1.0, float(len(reviews) / (mean_daily * 5))
                                ),
                                "review_count": len(reviews),
                            }
                        )

        except Exception as e:
            print(f"Error detecting review bombing: {e}")

        return anomalies

    def get_risk_factors(
        self, review_text: str, reviewer_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed risk factor breakdown
        """
        text_score = self._analyze_text_patterns(review_text)
        behavior_score = (
            self._analyze_reviewer_behavior(reviewer_data) if reviewer_data else 0.0
        )

        network_score = (
            self._simple_network_analysis(reviewer_data) if reviewer_data else 0.0
        )
        overall = float(
            min(
                1.0,
                max(
                    0.0,
                    text_score * 0.45 + behavior_score * 0.35 + network_score * 0.2,
                ),
            )
        )

        risk_factors = {
            # Keys expected by tests
            "text_suspicion": text_score,
            "behavior_suspicion": behavior_score,
            "network_suspicion": network_score,
            "overall_risk": overall,
            # Detailed breakdown
            "text_patterns": text_score,
            "reviewer_behavior": behavior_score,
            "account_age_risk": (
                self._assess_account_age_risk(reviewer_data) if reviewer_data else 0.0
            ),
            "review_frequency_risk": (
                self._assess_review_frequency_risk(reviewer_data)
                if reviewer_data
                else 0.0
            ),
            "profile_completeness": (
                self._assess_profile_completeness(reviewer_data)
                if reviewer_data
                else 0.0
            ),
        }

        return risk_factors

    def _assess_account_age_risk(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Assess risk based on account age
        """
        account_age = reviewer_data.get("account_age_days", 365)
        if account_age < 7:
            return 0.9
        elif account_age < 30:
            return 0.6
        elif account_age < 90:
            return 0.3
        else:
            return 0.1

    def _assess_review_frequency_risk(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Assess risk based on review frequency
        """
        account_age = reviewer_data.get("account_age_days", 365)
        review_count = reviewer_data.get("review_count", 0)

        if account_age > 0 and review_count > 0:
            reviews_per_day = review_count / account_age
            if reviews_per_day > 5:
                return 0.9
            elif reviews_per_day > 2:
                return 0.6
            elif reviews_per_day > 1:
                return 0.3
            else:
                return 0.1

        return 0.5

    def _assess_profile_completeness(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Assess risk based on profile completeness
        """
        completeness_score = 0
        total_fields = 4

        if reviewer_data.get("profile_photo", False):
            completeness_score += 1
        if reviewer_data.get("verified_email", False):
            completeness_score += 1
        if reviewer_data.get("verified_phone", False):
            completeness_score += 1
        if reviewer_data.get("bio", ""):
            completeness_score += 1

        incompleteness_ratio = 1 - (completeness_score / total_fields)
        return incompleteness_ratio * 0.5  # Scale down the impact
