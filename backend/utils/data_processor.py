import numpy as np  # type: ignore
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class DataProcessor:
    """
    Utility class for processing and generating sample data
    """

    def __init__(self):
        self.sample_locations = [
            "The Great Restaurant",
            "Amazing Cafe",
            "Perfect Bistro",
            "Lovely Diner",
            "Awesome Eatery",
            "Fantastic Food Court",
            "Incredible Kitchen",
        ]

        self.sample_review_texts = [
            "Great food and excellent service. Would definitely recommend!",
            "Average experience, nothing special but not bad either.",
            "Terrible service and food was cold. Will not be returning.",
            "Outstanding meal! Best restaurant in town, highly recommended.",
            "Decent place for a quick bite. Fair prices and good portions.",
        ]

    def generate_trend_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Generate sample trend data for trust scores over time.

        Args:
            days: Number of days to generate data for

        Returns:
            List of dictionaries containing trend data
        """
        base_date = datetime.now() - timedelta(days=days)
        trend_data: List[Dict[str, Any]] = []

        base_trust = 0.7
        for i in range(days):
            # Add some realistic variation
            daily_variation = random.uniform(-0.1, 0.1)
            trust_score = base_trust + daily_variation

            # Simulate weekend effects
            current_date = base_date + timedelta(days=i)
            if current_date.weekday() >= 5:  # Weekend
                trust_score += 0.05

            # Clamp after all adjustments
            trust_score = max(0.0, min(1.0, trust_score))

            trend_data.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "trust_score": round(trust_score, 3),
                    "review_count": random.randint(5, 25),
                    # Ensure rating stays within [1.0, 5.0]
                    "average_rating": max(
                        1.0, min(5.0, round(random.uniform(3.5, 4.8), 1))
                    ),
                }
            )

            # Update base trust slightly for next day
            base_trust = trust_score + random.uniform(-0.02, 0.02)

        return trend_data

    def get_sample_trusted_reviews(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate sample trusted reviews.

        Args:
            count: Number of trusted reviews to generate

        Returns:
            List of dictionaries containing trusted review data
        """
        trusted_reviews: List[Dict[str, Any]] = []

        for i in range(count):
            review: Dict[str, Any] = {
                "id": f"review_{i+1}",
                "text": random.choice(
                    [
                        "Excellent food quality and attentive service. The atmosphere was perfect for our date night. Highly recommend the seafood pasta!",
                        "Great value for money. Fresh ingredients and generous portions. Staff was friendly and accommodating.",
                        "Outstanding experience from start to finish. The chef clearly knows what they're doing. Will definitely return.",
                        "Perfect spot for lunch meetings. Quiet environment, professional service, and delicious food.",
                        "Family-friendly restaurant with something for everyone. Kids loved the pizza, adults enjoyed the wine selection.",
                    ]
                ),
                "trust_score": round(random.uniform(0.8, 0.95), 3),
                "rating": random.randint(4, 5),
                "date": (
                    datetime.now() - timedelta(days=random.randint(1, 30))
                ).strftime("%Y-%m-%d"),
                "reviewer": {
                    "name": f"TrustedUser{i+1}",
                    "review_count": random.randint(15, 100),
                    "account_age_days": random.randint(200, 1000),
                    "verified": True,
                },
            }
            trusted_reviews.append(review)

        return trusted_reviews

    def get_sample_flagged_reviews(self, count: int = 3) -> List[Dict[str, Any]]:
        """
        Generate sample flagged/suspicious reviews.

        Args:
            count: Number of flagged reviews to generate

        Returns:
            List of dictionaries containing flagged review data
        """
        flagged_reviews: List[Dict[str, Any]] = []

        suspicious_texts = [
            "Amazing amazing amazing! Best place ever! Perfect perfect perfect!",
            "Terrible worst experience ever never going back horrible horrible",
            "Good food nice place recommend",
            "This place is absolutely amazing perfect excellent outstanding wonderful fantastic great",
            "Worst service terrible food awful experience disgusting never again",
        ]

        for i in range(count):
            review: Dict[str, Any] = {
                "id": f"flagged_{i+1}",
                "text": random.choice(suspicious_texts),
                "trust_score": round(random.uniform(0.1, 0.3), 3),
                "rating": random.choice([1, 5]),  # Extreme ratings are suspicious
                "date": (
                    datetime.now() - timedelta(days=random.randint(1, 7))
                ).strftime("%Y-%m-%d"),
                "reviewer": {
                    "name": f"SuspiciousUser{i+1}",
                    "review_count": random.randint(0, 5),
                    "account_age_days": random.randint(1, 30),
                    "verified": False,
                },
                "flags": [
                    random.choice(
                        [
                            "Repetitive language",
                            "Extreme sentiment",
                            "New account activity",
                            "Generic content",
                            "Suspicious timing",
                        ]
                    )
                ],
            }
            flagged_reviews.append(review)

        return flagged_reviews

    def get_sample_reviewer_activity(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate sample reviewer activity history.

        Args:
            count: Number of activity records to generate

        Returns:
            List of dictionaries containing activity data, sorted by date
        """
        activities: List[Dict[str, Any]] = []

        activity_types = [
            "Posted review",
            "Updated profile",
            "Verified email",
            "Added photo",
            "Liked review",
            "Reported review",
        ]

        for i in range(count):
            activity: Dict[str, Any] = {
                "date": (
                    datetime.now() - timedelta(days=random.randint(1, 90))
                ).strftime("%Y-%m-%d"),
                "type": random.choice(activity_types),
                "location": random.choice(self.sample_locations),
                "trust_impact": random.choice(["positive", "neutral", "negative"]),
                "details": f"Activity {i+1} performed successfully",
            }
            activities.append(activity)

        return sorted(activities, key=lambda x: x["date"], reverse=True)

    def generate_sample_reviews(self, count: int = 20) -> List[Dict[str, Any]]:
        """
        Generate a set of sample reviews for testing.

        Args:
            count: Number of sample reviews to generate

        Returns:
            List of dictionaries containing sample review data
        """
        reviews: List[Dict[str, Any]] = []

        for i in range(count):
            # Generate realistic reviewer data
            account_age = random.randint(1, 1000)
            review_count = random.randint(0, 200)

            reviewer_data: Dict[str, Any] = {
                "id": f"user_{i+1}",
                "account_age_days": account_age,
                "review_count": review_count,
                "profile_photo": random.choice([True, False]),
                "verified_email": random.choice([True, False]),
                "verified_phone": random.choice([True, False]),
                "bio": "Food enthusiast" if random.random() > 0.5 else "",
                "location_diversity": random.uniform(0.1, 1.0),
                "recent_reviews": [],
            }

            # Generate review text with varying quality
            if random.random() < 0.7:  # 70% good reviews
                text = random.choice(
                    [
                        "Really enjoyed our dinner here. The service was prompt and the food was delicious. Great atmosphere for a night out.",
                        "Solid restaurant with good food and reasonable prices. Staff was friendly and helpful.",
                        "Had a wonderful experience. The pasta was perfectly cooked and the wine selection was excellent.",
                        "Family-friendly place with great food. Kids menu had good options and adults enjoyed their meals too.",
                        "Beautiful restaurant with amazing views. Food quality matched the ambiance perfectly.",
                    ]
                )
            else:  # 30% suspicious reviews
                text = random.choice(
                    [
                        "Amazing amazing best place ever!!!",
                        "Terrible worst food ever never going back",
                        "Perfect excellent outstanding wonderful",
                        "Good food nice staff",
                        "Bad service awful experience horrible",
                    ]
                )

            review: Dict[str, Any] = {
                "text": text,
                "reviewer_data": reviewer_data,
                "location_data": {
                    "id": f"location_{random.randint(1, 10)}",
                    "name": random.choice(self.sample_locations),
                    "category": random.choice(
                        ["Restaurant", "Cafe", "Fast Food", "Fine Dining"]
                    ),
                },
                "timestamp": (
                    datetime.now() - timedelta(days=random.randint(1, 365))
                ).isoformat(),
                "rating": random.randint(1, 5),
            }

            reviews.append(review)

        return reviews

    def calculate_statistics(
        self, reviews_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate statistical summaries for reviews.

        Args:
            reviews_data: List of review dictionaries to analyse

        Returns:
            Dictionary containing statistical analysis of the reviews
        """
        if not reviews_data:
            return {}

        trust_scores = [r.get("trust_score", 0.5) for r in reviews_data]
        ratings = [r.get("rating", 3) for r in reviews_data]

        stats: Dict[str, Any] = {
            "total_reviews": len(reviews_data),
            "average_trust_score": (
                round(float(np.mean(trust_scores)), 3) if trust_scores else 0.5
            ),
            "trust_score_std": (
                round(float(np.std(trust_scores)), 3) if trust_scores else 0.0
            ),
            "average_rating": round(float(np.mean(ratings)), 2) if ratings else 3.0,
            "trust_distribution": {
                "high_trust": sum(1 for score in trust_scores if score >= 0.7),
                "medium_trust": sum(1 for score in trust_scores if 0.4 <= score < 0.7),
                "low_trust": sum(1 for score in trust_scores if score < 0.4),
            },
            "rating_distribution": {
                "5_star": sum(1 for r in ratings if r == 5),
                "4_star": sum(1 for r in ratings if r == 4),
                "3_star": sum(1 for r in ratings if r == 3),
                "2_star": sum(1 for r in ratings if r == 2),
                "1_star": sum(1 for r in ratings if r == 1),
            },
        }

        return stats

    def export_analysis_results(
        self, analysis_results: List[Dict[str, Any]], filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export analysis results to a formatted structure.

        Args:
            analysis_results: List of analysis result dictionaries
            filename: Optional filename for the export

        Returns:
            Dictionary containing formatted export data
        """
        if not filename:
            filename = (
                f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        export_data: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_analyzed": len(analysis_results),
                "average_trust_score": float(
                    np.mean([r.get("trust_score", 0) for r in analysis_results])
                ),
                "suspicious_count": sum(
                    1 for r in analysis_results if r.get("trust_score", 1) < 0.3
                ),
                "trusted_count": sum(
                    1 for r in analysis_results if r.get("trust_score", 0) > 0.7
                ),
            },
            "detailed_results": analysis_results,
            "metadata": {
                "version": "1.0.0",
                "analysis_type": "review_trust_assessment",
                "filename": filename,
            },
        }

        return export_data
