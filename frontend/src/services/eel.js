// Eel service for communication with Python backend
class EelService {
  constructor() {
    this.isEelAvailable = typeof window !== "undefined" && window.eel;
  }

  async analyzeReview(reviewText, reviewerData = null, locationData = null) {
    if (!this.isEelAvailable) {
      console.warn("Eel not available, using mock data");
      return this.getMockAnalysis();
    }

    try {
      const result = await window.eel.analyze_review(
        reviewText,
        reviewerData,
        locationData
      )();
      return result;
    } catch (error) {
      console.error("Error analyzing review:", error);
      return { success: false, error: error.message };
    }
  }

  async analyzeBulkReviews(reviewsData) {
    if (!this.isEelAvailable) {
      console.warn("Eel not available, using mock data");
      return this.getMockBulkAnalysis();
    }

    try {
      const result = await window.eel.analyze_bulk_reviews(reviewsData)();
      return result;
    } catch (error) {
      console.error("Error analyzing bulk reviews:", error);
      return { success: false, error: error.message };
    }
  }

  async getTrustDashboardData(locationId) {
    if (!this.isEelAvailable) {
      console.warn("Eel not available, using mock data");
      return this.getMockDashboardData();
    }

    try {
      const result = await window.eel.get_trust_dashboard_data(locationId)();
      return result;
    } catch (error) {
      console.error("Error getting dashboard data:", error);
      return { success: false, error: error.message };
    }
  }

  async verifyImageAuthenticity(imageData, locationData) {
    if (!this.isEelAvailable) {
      console.warn("Eel not available, using mock data");
      return this.getMockImageAnalysis();
    }

    try {
      const result = await window.eel.verify_image_authenticity(
        imageData,
        locationData
      )();
      return result;
    } catch (error) {
      console.error("Error verifying image:", error);
      return { success: false, error: error.message };
    }
  }

  async getReviewerTrustProfile(reviewerId) {
    if (!this.isEelAvailable) {
      console.warn("Eel not available, using mock data");
      return this.getMockReviewerProfile();
    }

    try {
      const result = await window.eel.get_reviewer_trust_profile(reviewerId)();
      return result;
    } catch (error) {
      console.error("Error getting reviewer profile:", error);
      return { success: false, error: error.message };
    }
  }

  // Mock data for development
  getMockAnalysis() {
    return {
      success: true,
      trust_score: 0.78,
      sentiment_score: {
        polarity: 0.6,
        subjectivity: 0.7,
        overall_score: 0.65,
        confidence: 0.8,
      },
      authenticity_score: 0.82,
      fake_probability: 0.15,
      analysis: {
        sentiment: {
          category: "positive",
          intensity: 0.6,
          manipulation_indicators: 0.1,
          authenticity_score: 0.9,
        },
        authenticity_factors: {
          linguistic_quality: 0.8,
          sentiment_consistency: 0.85,
          length_appropriate: 0.9,
          spam_indicators: 0.95,
        },
        risk_factors: {
          text_patterns: 0.1,
          reviewer_behavior: 0.2,
          account_age_risk: 0.1,
          review_frequency_risk: 0.05,
          profile_completeness: 0.1,
        },
      },
    };
  }

  getMockBulkAnalysis() {
    return {
      success: true,
      location_trust_score: 0.72,
      summary: {
        total_reviews: 25,
        trusted_reviews: 18,
        suspicious_reviews: 3,
      },
      trust_trends: Array.from({ length: 30 }, (_, i) => ({
        timestamp: new Date(
          Date.now() - (29 - i) * 24 * 60 * 60 * 1000
        ).toISOString(),
        trust_score: 0.6 + Math.random() * 0.3,
      })),
      anomalies: [
        {
          timestamp: new Date(
            Date.now() - 5 * 24 * 60 * 60 * 1000
          ).toISOString(),
          trust_score: 0.2,
          anomaly_type: "review_bombing",
          severity: 0.8,
          review_count: 15,
        },
      ],
    };
  }

  getMockDashboardData() {
    return {
      success: true,
      location_id: "mock_location_123",
      overall_trust_score: 0.78,
      total_reviews: 1247,
      trust_distribution: {
        high_trust: 62,
        medium_trust: 28,
        low_trust: 10,
      },
      trend_data: Array.from({ length: 30 }, (_, i) => ({
        date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000)
          .toISOString()
          .split("T")[0],
        trust_score: 0.6 + Math.random() * 0.3,
        review_count: Math.floor(Math.random() * 20) + 5,
        average_rating: 3.5 + Math.random() * 1.5,
      })),
      risk_factors: {
        fake_review_probability: 0.15,
        reviewer_network_anomalies: 2,
        temporal_anomalies: 1,
      },
      top_trusted_reviews: [
        {
          id: "review_1",
          text: "Excellent food quality and attentive service. The atmosphere was perfect for our date night.",
          trust_score: 0.92,
          rating: 5,
          date: "2025-08-25",
        },
      ],
      flagged_reviews: [
        {
          id: "flagged_1",
          text: "Amazing amazing best place ever!!!",
          trust_score: 0.15,
          rating: 5,
          date: "2025-08-28",
          flags: ["Repetitive language", "Extreme sentiment"],
        },
      ],
    };
  }

  getMockImageAnalysis() {
    return {
      success: true,
      authenticity_score: 0.85,
      location_match: true,
      metadata_analysis: {
        timestamp_valid: true,
        geolocation_match: true,
        device_consistent: true,
      },
      visual_analysis: {
        quality_score: 0.9,
        manipulation_detected: false,
        content_relevance: 0.8,
      },
    };
  }

  getMockReviewerProfile() {
    return {
      success: true,
      reviewer_id: "mock_reviewer_123",
      trust_score: 0.72,
      review_count: 89,
      account_age_days: 456,
      verification_status: "verified",
      behavioral_analysis: {
        review_frequency: "normal",
        sentiment_consistency: 0.78,
        location_diversity: 0.85,
        network_analysis: "clean",
      },
      recent_activity: [
        {
          date: "2025-08-28",
          type: "Posted review",
          location: "Amazing Cafe",
          trust_impact: "positive",
        },
      ],
    };
  }
}

export default new EelService();
