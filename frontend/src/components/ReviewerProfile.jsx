import React, { useState } from "react";
import { User, Shield, Calendar, Activity, Star } from "lucide-react";
import eelService from "../services/eel";

const ReviewerProfile = () => {
  const [reviewerId, setReviewerId] = useState("reviewer_123");
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadProfile = async () => {
    if (!reviewerId.trim()) return;

    setLoading(true);
    try {
      const result = await eelService.getReviewerTrustProfile(reviewerId);
      if (result.success) {
        setProfile(result);
      }
    } catch (error) {
      console.error("Error loading reviewer profile:", error);
    } finally {
      setLoading(false);
    }
  };

  const getTrustScoreColor = (score) => {
    if (score >= 0.7) return "text-green-600 bg-green-50 border-green-200";
    if (score >= 0.4) return "text-yellow-600 bg-yellow-50 border-yellow-200";
    return "text-red-600 bg-red-50 border-red-200";
  };

  const getVerificationBadge = (status) => {
    switch (status) {
      case "verified":
        return (
          <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
            Verified
          </span>
        );
      case "pending":
        return (
          <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full">
            Pending
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">
            Unverified
          </span>
        );
    }
  };

  const getBehaviorColor = (value) => {
    if (typeof value === "string") {
      switch (value) {
        case "normal":
        case "clean":
          return "text-green-600";
        case "moderate":
          return "text-yellow-600";
        case "suspicious":
        case "high":
          return "text-red-600";
        default:
          return "text-gray-600";
      }
    }
    if (value >= 0.7) return "text-green-600";
    if (value >= 0.4) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Reviewer Trust Profile
        </h2>
        <p className="text-gray-600">
          Comprehensive analysis of reviewer credibility and behavior patterns
        </p>
      </div>

      {/* Search Section */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <User className="h-5 w-5 mr-2 text-primary-600" />
          Reviewer Lookup
        </h3>

        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="text"
              value={reviewerId}
              onChange={(e) => setReviewerId(e.target.value)}
              placeholder="Enter reviewer ID or username..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            onClick={loadProfile}
            disabled={loading || !reviewerId.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Loading...
              </>
            ) : (
              <>
                <Shield className="h-4 w-4 mr-2" />
                Analyse Profile
              </>
            )}
          </button>
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          <span className="text-sm text-gray-500">Quick lookup:</span>
          {["reviewer_123", "user_456", "foodie_789"].map((id) => (
            <button
              key={id}
              onClick={() => setReviewerId(id)}
              className="text-sm text-primary-600 hover:text-primary-700 underline"
            >
              {id}
            </button>
          ))}
        </div>
      </div>

      {/* Profile Results */}
      {profile && (
        <div className="space-y-6">
          {/* Profile Header */}
          <div className="card">
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex items-center justify-center">
                  <User className="h-8 w-8 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">
                    Reviewer ID: {profile.reviewer_id}
                  </h3>
                  <div className="flex items-center space-x-2 mt-1">
                    {getVerificationBadge(profile.verification_status)}
                    <span className="text-sm text-gray-500">
                      {profile.account_age_days} days old
                    </span>
                  </div>
                </div>
              </div>

              <div
                className={`px-4 py-3 rounded-lg border ${getTrustScoreColor(
                  profile.trust_score
                )}`}
              >
                <div className="text-center">
                  <div className="text-2xl font-bold">
                    {(profile.trust_score * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm opacity-75">Trust Score</div>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-blue-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-blue-600">
                    Total Reviews
                  </p>
                  <p className="text-2xl font-bold text-blue-900">
                    {profile.review_count}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <div className="flex items-center">
                <Calendar className="h-8 w-8 text-purple-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-purple-600">
                    Account Age
                  </p>
                  <p className="text-2xl font-bold text-purple-900">
                    {Math.floor(profile.account_age_days / 30)} months
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <div className="flex items-center">
                <Activity className="h-8 w-8 text-green-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-green-600">
                    Activity Level
                  </p>
                  <p className="text-2xl font-bold text-green-900">
                    {(
                      profile.review_count /
                      (profile.account_age_days / 30)
                    ).toFixed(1)}
                    /mo
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Behavioral Analysis */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Behavioral Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium text-gray-700">
                    Review Frequency
                  </span>
                  <span
                    className={`text-sm font-semibold ${getBehaviorColor(
                      profile.behavioral_analysis.review_frequency
                    )}`}
                  >
                    {profile.behavioral_analysis.review_frequency}
                  </span>
                </div>

                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium text-gray-700">
                    Sentiment Consistency
                  </span>
                  <span
                    className={`text-sm font-semibold ${getBehaviorColor(
                      profile.behavioral_analysis.sentiment_consistency
                    )}`}
                  >
                    {(
                      profile.behavioral_analysis.sentiment_consistency * 100
                    ).toFixed(0)}
                    %
                  </span>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium text-gray-700">
                    Location Diversity
                  </span>
                  <span
                    className={`text-sm font-semibold ${getBehaviorColor(
                      profile.behavioral_analysis.location_diversity
                    )}`}
                  >
                    {(
                      profile.behavioral_analysis.location_diversity * 100
                    ).toFixed(0)}
                    %
                  </span>
                </div>

                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium text-gray-700">
                    Network Analysis
                  </span>
                  <span
                    className={`text-sm font-semibold ${getBehaviorColor(
                      profile.behavioral_analysis.network_analysis
                    )}`}
                  >
                    {profile.behavioral_analysis.network_analysis}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
            <div className="space-y-3">
              {profile.recent_activity.map((activity, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded"
                >
                  <div className="flex items-center space-x-3">
                    <div
                      className={`w-2 h-2 rounded-full ${
                        activity.trust_impact === "positive"
                          ? "bg-green-500"
                          : activity.trust_impact === "negative"
                          ? "bg-red-500"
                          : "bg-gray-400"
                      }`}
                    />
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {activity.type}
                      </p>
                      <p className="text-xs text-gray-500">
                        {activity.location || "General activity"}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-900">{activity.date}</p>
                    <p
                      className={`text-xs ${
                        activity.trust_impact === "positive"
                          ? "text-green-600"
                          : activity.trust_impact === "negative"
                          ? "text-red-600"
                          : "text-gray-500"
                      }`}
                    >
                      {activity.trust_impact}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Trust Factors Breakdown */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">
              Trust Factors Breakdown
            </h3>
            <div className="space-y-4">
              {[
                {
                  label: "Account Maturity",
                  value: Math.min(1, profile.account_age_days / 365),
                },
                {
                  label: "Review Volume",
                  value: Math.min(1, profile.review_count / 100),
                },
                {
                  label: "Behavioral Consistency",
                  value: profile.behavioral_analysis.sentiment_consistency,
                },
                {
                  label: "Location Diversity",
                  value: profile.behavioral_analysis.location_diversity,
                },
                {
                  label: "Verification Status",
                  value: profile.verification_status === "verified" ? 1 : 0.5,
                },
              ].map((factor, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700 flex-1">
                    {factor.label}
                  </span>
                  <div className="flex items-center space-x-3 flex-1">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          factor.value >= 0.7
                            ? "bg-green-500"
                            : factor.value >= 0.4
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${factor.value * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-gray-900 w-12 text-right">
                      {(factor.value * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Default State */}
      {!profile && !loading && (
        <div className="text-center py-12">
          <User className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No Profile Loaded
          </h3>
          <p className="text-gray-500">
            Enter a reviewer ID and click &quot;Analyze Profile&quot; to view
            detailed trust analysis
          </p>
        </div>
      )}
    </div>
  );
};

export default ReviewerProfile;
