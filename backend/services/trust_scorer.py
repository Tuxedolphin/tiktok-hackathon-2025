import numpy as np  # type: ignore
from typing import Dict, List, Optional, Any


class TrustScorer:
    """
    Calculates comprehensive trust scores for reviews and locations
    """

    def __init__(self):
        # Weights for different trust factors
        self.weights = {
            "authenticity": 0.25,
            "sentiment_quality": 0.20,
            "reviewer_credibility": 0.25,
            "content_quality": 0.15,
            "temporal_consistency": 0.15,
        }

    def calculate_trust_score(
        self,
        review_text: str,
        sentiment_score: Dict[str, Any],
        authenticity_score: float,
        fake_probability: float,
        reviewer_data: Optional[Dict[str, Any]] = None,
        location_data: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Calculate comprehensive trust score for a review
        """
        try:
            # Base scores from ML models
            base_authenticity = authenticity_score
            sentiment_quality = self._assess_sentiment_quality(sentiment_score)
            content_quality = self._assess_content_quality(review_text)

            # Reviewer credibility
            reviewer_credibility = 1.0
            if reviewer_data:
                reviewer_credibility = self._calculate_reviewer_credibility(
                    reviewer_data
                )

            # Temporal consistency
            temporal_consistency = self._assess_temporal_consistency(
                reviewer_data, location_data
            )

            # Inverse of fake probability
            fake_adjusted_authenticity = max(0.0, 1.0 - fake_probability)

            # Combine authenticity scores
            combined_authenticity = (base_authenticity + fake_adjusted_authenticity) / 2

            # Calculate weighted trust score
            trust_score = (
                combined_authenticity * self.weights["authenticity"]
                + sentiment_quality * self.weights["sentiment_quality"]
                + reviewer_credibility * self.weights["reviewer_credibility"]
                + content_quality * self.weights["content_quality"]
                + temporal_consistency * self.weights["temporal_consistency"]
            )

            # Apply penalty for extremely suspicious reviews
            if fake_probability > 0.8:
                trust_score *= 0.5

            return max(0.0, min(1.0, trust_score))

        except Exception as e:
            print(f"Error calculating trust score: {e}")
            return 0.5

    def _assess_sentiment_quality(self, sentiment_analysis: Dict[str, Any]) -> float:
        """
        Assess the quality and authenticity of sentiment.

        Args:
            sentiment_analysis: Dictionary containing sentiment analysis results

        Returns:
            Quality score between 0.0 and 1.0
        """
        try:
            confidence = sentiment_analysis.get("confidence", 0.5)
            subjectivity = sentiment_analysis.get("subjectivity", 0.5)

            # Higher confidence and appropriate subjectivity indicate better quality
            quality_score = confidence * 0.7 + (1 - abs(subjectivity - 0.5)) * 0.3

            return min(1.0, max(0.0, quality_score))

        except Exception:
            return 0.5

    def _assess_content_quality(self, text: str) -> float:
        """
        Assess the quality of review content
        """
        try:
            if not text or len(text.strip()) < 5:
                return 0.2

            quality_score = 1.0

            # Length appropriateness
            word_count = len(text.split())
            if 10 <= word_count <= 150:
                length_score = 1.0
            elif 5 <= word_count <= 200:
                length_score = 0.8
            else:
                length_score = 0.4

            # Information density (specific vs generic)
            specific_indicators = [
                "time",
                "date",
                "price",
                "name",
                "location",
                "menu",
                "staff",
                "atmosphere",
                "service",
                "quality",
                "experience",
                "recommend",
            ]

            specificity_count = sum(
                1
                for indicator in specific_indicators
                if indicator.lower() in text.lower()
            )
            specificity_score = min(1.0, specificity_count / 5)

            # Readability (simple heuristic)
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            if sentences:
                avg_sentence_length = np.mean([len(s.split()) for s in sentences])
                if 5 <= avg_sentence_length <= 25:
                    readability_score = 1.0
                else:
                    readability_score = 0.7
            else:
                readability_score = 0.5

            # Combine quality factors
            quality_score = (
                length_score * 0.4 + specificity_score * 0.4 + readability_score * 0.2
            )

            return max(0.0, min(1.0, quality_score))

        except Exception:
            return 0.5

    def _calculate_reviewer_credibility(self, reviewer_data: Dict[str, Any]) -> float:
        """
        Calculate reviewer credibility score
        """
        try:
            credibility_score = 0.5  # Base score

            # Account age factor
            account_age = reviewer_data.get("account_age_days", 0)
            if account_age > 365:
                age_score = 1.0
            elif account_age > 180:
                age_score = 0.8
            elif account_age > 90:
                age_score = 0.6
            elif account_age > 30:
                age_score = 0.4
            else:
                age_score = 0.2

            # Review history
            review_count = reviewer_data.get("review_count", 0)
            if review_count > 50:
                history_score = 1.0
            elif review_count > 20:
                history_score = 0.8
            elif review_count > 10:
                history_score = 0.6
            elif review_count > 5:
                history_score = 0.4
            else:
                history_score = 0.2

            # Profile completeness
            profile_score = 0.0
            if reviewer_data.get("profile_photo", False):
                profile_score += 0.25
            if reviewer_data.get("verified_email", False):
                profile_score += 0.25
            if reviewer_data.get("verified_phone", False):
                profile_score += 0.25
            if reviewer_data.get("bio", ""):
                profile_score += 0.25

            # Review diversity (different types of locations)
            diversity_score = min(1.0, reviewer_data.get("location_diversity", 0.5))

            # Combine credibility factors
            credibility_score = (
                age_score * 0.3
                + history_score * 0.3
                + profile_score * 0.2
                + diversity_score * 0.2
            )

            return max(0.0, min(1.0, credibility_score))

        except Exception:
            return 0.5

    def _assess_temporal_consistency(
        self,
        reviewer_data: Optional[Dict[str, Any]],
        location_data: Optional[Dict[str, Any]],
    ) -> float:
        """
        Assess temporal consistency of reviews
        """
        try:
            # This would analyze patterns like review timing, frequency, etc.
            # For now, implementing a simplified version

            consistency_score = 1.0

            if reviewer_data:
                # Check for unnatural review frequency
                account_age = reviewer_data.get("account_age_days", 365)
                review_count = reviewer_data.get("review_count", 0)

                if account_age > 0 and review_count > 0:
                    reviews_per_day = review_count / account_age

                    if reviews_per_day > 3:  # Too frequent
                        consistency_score -= 0.4
                    elif reviews_per_day > 1:
                        consistency_score -= 0.2

                # Check for review clustering (many reviews in short time)
                recent_reviews = reviewer_data.get("recent_reviews", [])
                if len(recent_reviews) > 5:
                    # Simple clustering detection
                    timestamps = [r.get("timestamp", "") for r in recent_reviews[-10:]]
                    # This would be more sophisticated in a real implementation
                    if (
                        len(set(t.split(" ")[0] for t in timestamps if t))
                        < len(timestamps) / 2
                    ):
                        consistency_score -= 0.3

            return max(0.0, min(1.0, consistency_score))

        except Exception:
            return 0.8  # Default good consistency

    def calculate_location_trust(self, review_results: List[Dict[str, Any]]) -> float:
        """
        Calculate overall trust score for a location based on all reviews
        """
        try:
            if not review_results:
                return 0.5

            successful_results = [r for r in review_results if r.get("success", False)]

            if not successful_results:
                return 0.5

            # Basic average with outlier handling
            trust_scores = [r["trust_score"] for r in successful_results]

            # Remove extreme outliers (bottom and top 5%)
            if len(trust_scores) > 20:
                sorted_scores = sorted(trust_scores)
                outlier_count = max(1, len(sorted_scores) // 20)
                trimmed_scores = sorted_scores[outlier_count:-outlier_count]
            else:
                trimmed_scores = trust_scores

            # Calculate weighted average (more recent reviews get higher weight)
            # For simplicity, using equal weights here
            location_trust = float(np.mean(trimmed_scores))

            # Apply confidence adjustment based on sample size
            confidence_adjustment = min(1.0, len(successful_results) / 50)
            adjusted_trust = location_trust * confidence_adjustment + 0.5 * (
                1 - confidence_adjustment
            )

            return max(0.0, min(1.0, float(adjusted_trust)))

        except Exception as e:
            print(f"Error calculating location trust: {e}")
            return 0.5

    def get_trust_category(self, trust_score: float) -> str:
        """
        Categorise trust score into readable labels.

        Args:
            trust_score: Trust score between 0.0 and 1.0

        Returns:
            String category describing the trust level
        """
        if trust_score >= 0.8:
            return "highly_trusted"
        elif trust_score >= 0.6:
            return "trusted"
        elif trust_score >= 0.4:
            return "moderate"
        elif trust_score >= 0.2:
            return "low_trust"
        else:
            return "untrusted"

    def get_trust_explanation(
        self, trust_score: float, components: Dict[str, Any]
    ) -> str:
        """
        Generate human-readable explanation of trust score.

        Args:
            trust_score: Trust score between 0.0 and 1.0
            components: Dictionary containing trust score components

        Returns:
            Human-readable explanation of the trust assessment
        """
        category = self.get_trust_category(trust_score)

        explanations = {
            "highly_trusted": "This review shows strong indicators of authenticity and reliability.",
            "trusted": "This review appears genuine with good credibility indicators.",
            "moderate": "This review has mixed trust signals and should be considered with caution.",
            "low_trust": "This review shows several suspicious patterns and may not be reliable.",
            "untrusted": "This review exhibits many characteristics of fake or manipulated content.",
        }

        base_explanation = explanations.get(category, "Trust assessment completed.")

        # Add specific factors
        factors: List[str] = []
        if components.get("authenticity_score", 0) < 0.3:
            factors.append("low authenticity score")
        if components.get("fake_probability", 0) > 0.7:
            factors.append("high fake probability")
        if components.get("reviewer_credibility", 1) < 0.3:
            factors.append("low reviewer credibility")

        if factors:
            base_explanation += f" Key concerns: {', '.join(factors)}."

        return base_explanation
