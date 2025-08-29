"""
Configuration constants for the Review Trust System.

Contains application-wide constants, thresholds, and configuration values
used across different components of the system.
"""

# Trust Score Thresholds
TRUST_THRESHOLD_HIGH = 0.7
TRUST_THRESHOLD_LOW = 0.3

# Sentiment Analysis Configuration
SENTIMENT_MANIPULATION_THRESHOLD = 0.3
SENTIMENT_VARIANCE_THRESHOLD = 0.01
EMOTIONAL_INTENSITY_MULTIPLIER = 0.1

# Fake Detection Thresholds
FAKE_PROBABILITY_HIGH = 0.8
FAKE_PROBABILITY_LOW = 0.2
REVIEW_LENGTH_MIN = 10
REVIEW_LENGTH_MAX = 2000

# Reviewer Behaviour Analysis
ACCOUNT_AGE_SUSPICIOUS_DAYS = 30
REVIEW_FREQUENCY_SUSPICIOUS = 5  # Reviews per day
VERIFICATION_SCORE_WEIGHTS = {
    "email": 0.3,
    "phone": 0.3,
    "profile_photo": 0.2,
    "social_links": 0.2,
}

# Trust Scorer Weights
TRUST_WEIGHTS = {
    "authenticity": 0.25,
    "sentiment_quality": 0.20,
    "reviewer_credibility": 0.25,
    "content_quality": 0.15,
    "temporal_consistency": 0.15,
}

# Application Configuration
DEFAULT_PORT = 8080
FRONTEND_PATH = "frontend/dist"
BROWSER_SIZE = (1200, 800)

# Data Processing
TREND_DATA_DEFAULT_DAYS = 30
SAMPLE_REVIEW_COUNT = 20
MAX_BULK_REVIEWS = 100

# API Response Codes
SUCCESS_CODE = 200
ERROR_CODE = 500
VALIDATION_ERROR_CODE = 400
