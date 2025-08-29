#!/usr/bin/env python3
import sys
from typing import Dict, List, Optional, Any, Union

# Make eel optional so tests and CLI can run without it
try:  # pragma: no cover - import guard
    import eel  # type: ignore

    _eel_available = True
except Exception:  # pragma: no cover - import guard
    _eel_available = False

    class _EelStub:
        def expose(self, f: Any) -> Any:  # type: ignore[no-redef]
            return f

        def init(self, *_args: Any, **_kwargs: Any) -> None:  # type: ignore[no-redef]
            return None

        def start(self, *_args: Any, **_kwargs: Any) -> None:  # type: ignore[no-redef]
            raise RuntimeError(
                "Eel is not available. Install 'eel' to run the desktop app."
            )

    eel = _EelStub()  # type: ignore

from backend.services.review_analyser import ReviewAnalyser
from backend.services.trust_scorer import TrustScorer
from backend.services.sentiment_analyser import SentimentAnalyser
from backend.services.fake_detector import FakeReviewDetector
from backend.utils.data_processor import DataProcessor
from backend.utils.logging_config import get_logger

logger = get_logger("main")

# Initialise ML services
review_analyser = ReviewAnalyser()
trust_scorer = TrustScorer()
sentiment_analyser = SentimentAnalyser()
fake_detector = FakeReviewDetector()
data_processor = DataProcessor()


@eel.expose
def analyze_review(
    review_text: str,
    reviewer_data: Optional[Dict[str, Any]] = None,
    location_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Main function to analyze a review's trustworthiness
    """
    try:
        # Process the review through multiple ML models
        sentiment_score = sentiment_analyser.analyse_sentiment(review_text)
        authenticity_score = review_analyser.calculate_authenticity(
            review_text, reviewer_data
        )
        fake_probability = fake_detector.detect_fake_review(review_text, reviewer_data)
        trust_score = trust_scorer.calculate_trust_score(
            review_text,
            sentiment_score,
            authenticity_score,
            fake_probability,
            reviewer_data,
            location_data,
        )

        return {
            "success": True,
            "trust_score": trust_score,
            "sentiment_score": sentiment_score,
            "authenticity_score": authenticity_score,
            "fake_probability": fake_probability,
            "analysis": {
                "sentiment": sentiment_analyser.get_sentiment_breakdown(review_text),
                "authenticity_factors": review_analyser.get_authenticity_factors(
                    review_text
                ),
                "risk_factors": fake_detector.get_risk_factors(
                    review_text, reviewer_data
                ),
            },
        }
    except Exception as e:
        logger.exception("analyze_review failed")
        return {"success": False, "error": str(e)}


@eel.expose
def analyze_bulk_reviews(reviews_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze multiple reviews for a location
    """
    try:
        results: List[Dict[str, Any]] = []
        trust_trends: List[Dict[str, Any]] = []

        for review in reviews_data:
            result = analyze_review(
                review.get("text", ""),
                review.get("reviewer_data"),
                review.get("location_data"),
            )
            results.append(result)
            if result.get("success"):
                trust_trends.append(
                    {
                        "timestamp": review.get("timestamp"),
                        "trust_score": result["trust_score"],
                    }
                )

        # Calculate location-level metrics
        location_trust_score = trust_scorer.calculate_location_trust(results)
        anomaly_detection = fake_detector.detect_temporal_anomalies(trust_trends)

        return {
            "success": True,
            "individual_results": results,
            "location_trust_score": location_trust_score,
            "trust_trends": trust_trends,
            "anomalies": anomaly_detection,
            "summary": {
                "total_reviews": len(reviews_data),
                "trusted_reviews": sum(
                    1 for r in results if r.get("trust_score", 0) > 0.7
                ),
                "suspicious_reviews": sum(
                    1 for r in results if r.get("trust_score", 0) < 0.3
                ),
            },
        }
    except Exception as e:
        logger.exception("analyze_bulk_reviews failed")
        return {"success": False, "error": str(e)}


@eel.expose
def get_trust_dashboard_data(location_id: str) -> Dict[str, Any]:
    """
    Get comprehensive trust dashboard data for a location
    """
    try:
        # This would typically fetch from a database
        # For demo purposes, we'll generate sample data
        return {
            "success": True,
            "location_id": location_id,
            "overall_trust_score": 0.78,
            "total_reviews": 1247,
            "trust_distribution": {
                "high_trust": 62,
                "medium_trust": 28,
                "low_trust": 10,
            },
            "trend_data": data_processor.generate_trend_data(),
            "risk_factors": {
                "fake_review_probability": 0.15,
                "reviewer_network_anomalies": 2,
                "temporal_anomalies": 1,
            },
            "top_trusted_reviews": data_processor.get_sample_trusted_reviews(),
            "flagged_reviews": data_processor.get_sample_flagged_reviews(),
        }
    except Exception as e:
        logger.exception("get_trust_dashboard_data failed")
        return {"success": False, "error": str(e)}


@eel.expose
def verify_image_authenticity(
    image_data: Union[str, bytes], location_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Verify authenticity of uploaded images
    """
    try:
        # Image verification would use computer vision models
        # For demo purposes, returning mock analysis
        return {
            "success": True,
            "authenticity_score": 0.85,
            "location_match": True,
            "metadata_analysis": {
                "timestamp_valid": True,
                "geolocation_match": True,
                "device_consistent": True,
            },
            "visual_analysis": {
                "quality_score": 0.9,
                "manipulation_detected": False,
                "content_relevance": 0.8,
            },
        }
    except Exception as e:
        logger.exception("verify_image_authenticity failed")
        return {"success": False, "error": str(e)}


@eel.expose
def get_reviewer_trust_profile(reviewer_id: str) -> Dict[str, Any]:
    """
    Get trust profile for a specific reviewer
    """
    try:
        return {
            "success": True,
            "reviewer_id": reviewer_id,
            "trust_score": 0.72,
            "review_count": 89,
            "account_age_days": 456,
            "verification_status": "verified",
            "behavioral_analysis": {
                "review_frequency": "normal",
                "sentiment_consistency": 0.78,
                "location_diversity": 0.85,
                "network_analysis": "clean",
            },
            "recent_activity": data_processor.get_sample_reviewer_activity(),
        }
    except Exception as e:
        logger.exception("get_reviewer_trust_profile failed")
        return {"success": False, "error": str(e)}


def start_app() -> None:
    """
    Start the Eel application
    """
    try:
        # Initialise web folder then start the web app
        eel.init("frontend/dist")
        eel.start("index.html", size=(1200, 800), port=8080)
    except Exception:
        logger.exception("Error starting application")
        sys.exit(1)


if __name__ == "__main__":
    start_app()
