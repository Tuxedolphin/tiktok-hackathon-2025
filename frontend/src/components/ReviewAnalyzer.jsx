import React, { useState } from "react";
import { Shield, Loader2 } from "lucide-react";
import eelService from "../services/eel";

const ReviewAnalyzer = () => {
  const [reviewText, setReviewText] = useState("");
  const [reviewerData, setReviewerData] = useState({
    account_age_days: 365,
    review_count: 25,
    profile_photo: true,
    verified_email: true,
    verified_phone: false,
    bio: "Food enthusiast",
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!reviewText.trim()) {
      setError("Please enter a review to analyse");
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const result = await eelService.analyzeReview(reviewText, reviewerData);

      if (result.success) {
        setAnalysis(result);
      } else {
        setError(result.error || "Failed to analyse review");
      }
    } catch (err) {
      setError("Error communicating with analysis service");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getTrustScoreColor = (score) => {
    if (score >= 0.7) return "text-green-600 bg-green-50 border-green-200";
    if (score >= 0.4) return "text-yellow-600 bg-yellow-50 border-yellow-200";
    return "text-red-600 bg-red-50 border-red-200";
  };

  const getTrustLabel = (score) => {
    if (score >= 0.8) return "Highly Trusted";
    if (score >= 0.6) return "Trusted";
    if (score >= 0.4) return "Moderate Trust";
    if (score >= 0.2) return "Low Trust";
    return "Untrusted";
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Single Review Analysis
        </h2>
        <p className="text-gray-600">
          Analyze individual reviews for authenticity and trustworthiness using
          advanced ML models
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Shield className="h-5 w-5 mr-2 text-primary-600" />
            Review Analysis
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Review Text *
              </label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Enter the review text to analyze..."
                className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Account Age (days)
                </label>
                <input
                  type="number"
                  value={reviewerData.account_age_days}
                  onChange={(e) =>
                    setReviewerData({
                      ...reviewerData,
                      account_age_days: parseInt(e.target.value) || 0,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Review Count
                </label>
                <input
                  type="number"
                  value={reviewerData.review_count}
                  onChange={(e) =>
                    setReviewerData({
                      ...reviewerData,
                      review_count: parseInt(e.target.value) || 0,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Reviewer Verification
              </label>

              <div className="space-y-2">
                {[
                  { key: "profile_photo", label: "Profile Photo" },
                  { key: "verified_email", label: "Verified Email" },
                  { key: "verified_phone", label: "Verified Phone" },
                ].map(({ key, label }) => (
                  <label key={key} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={reviewerData[key]}
                      onChange={(e) =>
                        setReviewerData({
                          ...reviewerData,
                          [key]: e.target.checked,
                        })
                      }
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">{label}</span>
                  </label>
                ))}
              </div>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !reviewText.trim()}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Analysing...
                </>
              ) : (
                <>
                  <Shield className="h-4 w-4 mr-2" />
                  Analyse Review
                </>
              )}
            </button>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Analysis Results</h3>

          {analysis ? (
            <div className="space-y-4">
              {/* Trust Score */}
              <div
                className={`p-4 rounded-lg border ${getTrustScoreColor(
                  analysis.trust_score
                )}`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold">Trust Score</h4>
                    <p className="text-sm opacity-75">
                      {getTrustLabel(analysis.trust_score)}
                    </p>
                  </div>
                  <div className="text-2xl font-bold">
                    {(analysis.trust_score * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* Detailed Scores */}
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium">
                    Authenticity Score
                  </span>
                  <span className="font-semibold">
                    {(analysis.authenticity_score * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium">Fake Probability</span>
                  <span
                    className={`font-semibold ${
                      analysis.fake_probability > 0.5
                        ? "text-red-600"
                        : "text-green-600"
                    }`}
                  >
                    {(analysis.fake_probability * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium">
                    Sentiment Confidence
                  </span>
                  <span className="font-semibold">
                    {(analysis.sentiment_score.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Risk Factors */}
              {analysis.analysis?.risk_factors && (
                <div>
                  <h4 className="font-semibold mb-2 text-gray-800">
                    Risk Factors
                  </h4>
                  <div className="space-y-2">
                    {Object.entries(analysis.analysis.risk_factors).map(
                      ([factor, score]) => (
                        <div
                          key={factor}
                          className="flex justify-between items-center text-sm"
                        >
                          <span className="capitalize text-gray-600">
                            {factor.replace(/_/g, " ")}
                          </span>
                          <div className="flex items-center">
                            <div className="w-16 h-2 bg-gray-200 rounded mr-2">
                              <div
                                className={`h-full rounded ${
                                  score > 0.6
                                    ? "bg-red-500"
                                    : score > 0.3
                                    ? "bg-yellow-500"
                                    : "bg-green-500"
                                }`}
                                style={{ width: `${score * 100}%` }}
                              />
                            </div>
                            <span className="font-medium">
                              {(score * 100).toFixed(0)}%
                            </span>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* Sentiment Analysis */}
              {analysis.analysis?.sentiment && (
                <div>
                  <h4 className="font-semibold mb-2 text-gray-800">
                    Sentiment Analysis
                  </h4>
                  <div className="bg-gray-50 p-3 rounded space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Category:</span>
                      <span
                        className={`text-sm font-medium capitalize ${
                          analysis.analysis.sentiment.category === "positive"
                            ? "text-green-600"
                            : analysis.analysis.sentiment.category ===
                              "negative"
                            ? "text-red-600"
                            : "text-gray-600"
                        }`}
                      >
                        {analysis.analysis.sentiment.category}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Intensity:</span>
                      <span className="text-sm font-medium">
                        {(analysis.analysis.sentiment.intensity * 100).toFixed(
                          0
                        )}
                        %
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Shield className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>
                Enter a review and click &quot;Analyse Review&quot; to see
                results
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReviewAnalyzer;
