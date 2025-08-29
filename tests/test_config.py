"""
Base test configuration and utilities for the Review Trust System test suite.
"""

import sys
import os
from typing import Dict, Any, List, Union

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Test data constants
SAMPLE_REVIEWS = {
    "positive": "This restaurant is absolutely amazing! The food is incredible and the service is outstanding. Highly recommend to everyone!",
    "negative": "Terrible experience! The food was cold, service was awful, and I would never come back. Waste of money!",
    "neutral": "The restaurant was decent. Food was okay, service was average. Nothing special but not bad either.",
    "short": "Good place.",
    "long": "I had an absolutely wonderful dining experience at this establishment. The ambiance was perfect for a romantic evening, with soft lighting and elegant decor that created a warm and inviting atmosphere. The staff was incredibly attentive and knowledgeable about the menu, providing excellent recommendations. The food was expertly prepared with fresh ingredients and beautiful presentation. I especially enjoyed the chef's special, which was a delightful fusion of flavors that exceeded my expectations. The wine selection was extensive and the sommelier helped us find the perfect pairing. Overall, this restaurant deserves its excellent reputation and I will definitely be returning soon.",
    "suspicious": "AMAZING AMAZING AMAZING! Best place ever! Perfect perfect perfect! Everyone must go here right now!!!",
    "fake_positive": "This is the best restaurant in the world! Everything is perfect and amazing! 5 stars!",
    "fake_negative": "Worst place ever! Terrible terrible terrible! Never go here! Awful!",
}

SAMPLE_REVIEWER_DATA: Dict[str, Dict[str, Union[int, bool, str, float]]] = {
    "trusted": {
        "account_age_days": 365,
        "review_count": 25,
        "verified_email": True,
        "profile_photo": True,
        "verified_phone": True,
        "bio": "Food enthusiast and travel blogger",
        "location_diversity": 0.8,
    },
    "suspicious": {
        "account_age_days": 5,
        "review_count": 1,
        "verified_email": False,
        "profile_photo": False,
        "verified_phone": False,
        "bio": "",
        "location_diversity": 0.1,
    },
    "moderate": {
        "account_age_days": 90,
        "review_count": 8,
        "verified_email": True,
        "profile_photo": False,
        "verified_phone": False,
        "bio": "Occasional reviewer",
        "location_diversity": 0.4,
    },
}

SAMPLE_LOCATION_DATA = {
    "restaurant": {
        "id": "loc_001",
        "name": "Test Restaurant",
        "category": "Fine Dining",
        "location": "New York, NY",
    }
}


def get_sample_trust_trends(days: int = 30) -> List[Dict[str, Any]]:
    """Generate sample trust trend data for testing."""
    import random
    from datetime import datetime, timedelta

    trends: List[Dict[str, Any]] = []
    base_date = datetime.now() - timedelta(days=days)

    for i in range(days):
        date = base_date + timedelta(days=i)
        trends.append(
            {
                "timestamp": date.isoformat(),
                "trust_score": round(random.uniform(0.3, 0.9), 3),
                "review_count": random.randint(1, 10),
            }
        )

    return trends
