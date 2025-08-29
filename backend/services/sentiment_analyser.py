import numpy as np  # type: ignore
from textblob import TextBlob  # type: ignore
import re
from typing import Dict, List, Any


class SentimentAnalyser:
    """
    Advanced sentiment analysis for review authenticity detection.

    Analyses emotional authenticity and detects manipulation patterns in review sentiment.
    """

    def __init__(self) -> None:
        self.sentiment_keywords = {
            "positive": [
                "excellent",
                "amazing",
                "wonderful",
                "fantastic",
                "great",
                "love",
                "perfect",
                "outstanding",
            ],
            "negative": [
                "terrible",
                "awful",
                "horrible",
                "worst",
                "hate",
                "disgusting",
                "disappointed",
            ],
            "neutral": ["okay", "average", "decent", "fine", "normal", "typical"],
        }

    def analyse_sentiment(self, text: Any) -> Dict[str, float]:
        """
        Comprehensive sentiment analysis
        """
        if not isinstance(text, str):
            # Let type errors propagate for tests expecting exceptions
            raise TypeError("text must be a string")
        try:
            blob = TextBlob(text)

            # Basic sentiment scores
            polarity = float(blob.sentiment.polarity)  # type: ignore # -1 to 1
            subjectivity = float(blob.sentiment.subjectivity)  # type: ignore # 0 to 1

            # Keyword-based sentiment
            keyword_sentiment = self._analyse_keyword_sentiment(text)

            # Combine different sentiment measures
            combined_sentiment: Dict[str, float] = {
                "polarity": polarity,
                "subjectivity": subjectivity,
                "keyword_sentiment": keyword_sentiment,
                "overall_score": (polarity + keyword_sentiment) / 2,
                "confidence": 1.0
                - abs(polarity - keyword_sentiment),  # Agreement between methods
            }

            # Enrich with intensity and manipulation score for compatibility with tests
            intensity = self._detect_emotional_intensity(text)
            manipulation = self._detect_sentiment_manipulation(text)
            combined_sentiment["intensity"] = float(max(0.0, min(1.0, intensity)))
            combined_sentiment["manipulation_score"] = float(
                max(0.0, min(1.0, manipulation))
            )

            return combined_sentiment

        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            fallback = {
                "polarity": 0.0,
                "subjectivity": 0.5,
                "keyword_sentiment": 0.0,
                "overall_score": 0.0,
                "confidence": 0.5,
            }
            # Include expected keys with safe defaults
            fallback["intensity"] = 0.0
            fallback["manipulation_score"] = 0.0
            return fallback

    def _analyse_keyword_sentiment(self, text: str) -> float:
        """
        Analyse sentiment based on keyword presence.

        Uses predefined sentiment keywords to calculate an alternative sentiment score
        that can be compared with TextBlob's analysis for consistency checking.
        """
        text_lower = text.lower()

        positive_count = sum(
            1 for word in self.sentiment_keywords["positive"] if word in text_lower
        )
        negative_count = sum(
            1 for word in self.sentiment_keywords["negative"] if word in text_lower
        )
        neutral_count = sum(
            1 for word in self.sentiment_keywords["neutral"] if word in text_lower
        )

        total_sentiment_words = positive_count + negative_count + neutral_count

        if total_sentiment_words == 0:
            return 0.0

        # Calculate weighted sentiment score
        sentiment_score = (positive_count - negative_count) / total_sentiment_words
        return sentiment_score

    # --- Backwards compatibility aliases (American spelling) ---
    def _analyze_keyword_sentiment(self, text: str) -> float:  # type: ignore
        return self._analyse_keyword_sentiment(text)

    def _calculate_sentiment_intensity(self, sentiment: Dict[str, float]) -> float:  # type: ignore
        # Older tests expect intensity to be derived from polarity & subjectivity
        # Use a simple combination and clamp to [0,1]
        polarity = float(sentiment.get("polarity", 0.0))
        subjectivity = float(sentiment.get("subjectivity", 0.5))
        raw = (abs(polarity) * 0.6) + (subjectivity * 0.4)
        return float(max(0.0, min(1.0, raw)))

    def get_sentiment_breakdown(self, text: str) -> Dict[str, Any]:
        """
        Get detailed sentiment breakdown
        """
        analysis = self.analyse_sentiment(text)

        # Categorize sentiment
        polarity = analysis["polarity"]
        if polarity > 0.1:
            category = "positive"
        elif polarity < -0.1:
            category = "negative"
        else:
            category = "neutral"

        # Detect emotional intensity
        intensity = self._detect_emotional_intensity(text)

        # Check for sentiment manipulation indicators
        manipulation_score = self._detect_sentiment_manipulation(text)

        return {
            "category": category,
            "intensity": intensity,
            "manipulation_indicators": manipulation_score,
            "authenticity_score": max(0.0, 1.0 - manipulation_score),
            "raw_analysis": analysis,
        }

    def _detect_emotional_intensity(self, text: str) -> float:
        """
        Detect emotional intensity in the text
        """
        # Count exclamation marks and caps
        exclamation_count = text.count("!")
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0

        # Emotional word patterns
        intense_words = [
            "absolutely",
            "completely",
            "totally",
            "extremely",
            "incredibly",
            "unbelievably",
        ]
        intense_count = sum(1 for word in intense_words if word.lower() in text.lower())

        # Calculate intensity score (0-1)
        intensity = min(
            1.0, (exclamation_count * 0.1 + caps_ratio + intense_count * 0.1)
        )

        return intensity

    def _detect_sentiment_manipulation(self, text: str) -> float:
        """
        Detect sentiment manipulation in review text.

        Args:
            text: Review text to analyse

        Returns:
            Manipulation score between 0.0 and 1.0
        """
        manipulation_score = 0.0

        # Excessive positive/negative words
        blob = TextBlob(text)
        words = [str(word) for word in blob.words]  # type: ignore # Convert to list of strings

        if len(words) > 0:
            # Check for repetitive sentiment patterns
            sentiment_words: List[float] = []
            for word in words:
                word_sentiment = float(TextBlob(word).sentiment.polarity)  # type: ignore
                if abs(word_sentiment) > 0.3:
                    sentiment_words.append(word_sentiment)

            if len(sentiment_words) > 0:
                # High density of sentiment words might indicate manipulation
                sentiment_density = len(sentiment_words) / len(words)
                if sentiment_density > 0.3:
                    manipulation_score += 0.35

                # Check for unnatural sentiment consistency
                sentiment_variance = float(
                    np.var(sentiment_words) if len(sentiment_words) > 1 else 0
                )
                if sentiment_variance < 0.01 and len(sentiment_words) > 3:
                    manipulation_score += 0.25

        # Detect template-like patterns
        template_patterns = [
            r"(would recommend|highly recommend).*(would recommend|highly recommend)",
            r"(best \w+).*(best \w+)",
            r"(never go back|never return).*(never go back|never return)",
        ]

        for pattern in template_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                manipulation_score += 0.2

        # Repetition of the same word multiple times (e.g., "amazing amazing amazing")
        if re.search(r"\b(\w+)\b(?:\s+\1\b){2,}", text, re.IGNORECASE):
            manipulation_score += 0.2

        # Many exclamation marks or shouting in caps can indicate hypey manipulation
        if text.count("!") >= 3:
            manipulation_score += 0.1

        return min(1.0, manipulation_score)
