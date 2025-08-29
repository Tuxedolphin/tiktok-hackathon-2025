import React, { useState } from "react";
import {
  FileText,
  BarChart3,
  AlertTriangle,
  CheckCircle,
  Loader2,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import eelService from "../services/eel";

const BulkAnalyzer = () => {
  const [reviews, setReviews] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const sampleReviews = `Amazing food and excellent service! Highly recommend this place.
Terrible experience, food was cold and service was slow.
Great atmosphere and delicious meals. Perfect for date night.
Worst restaurant ever! Never going back!!!
Decent place with good value for money. Staff was friendly.
Absolutely perfect excellent outstanding amazing wonderful!
Food was okay, nothing special but not bad either.
AMAZING AMAZING AMAZING BEST PLACE EVER!!!
Really enjoyed our dinner here. Fresh ingredients and great portions.
Horrible awful terrible disgusting never again worst service.`;

  const handleAnalyze = async () => {
    if (!reviews.trim()) {
      setError("Please enter reviews to analyse");
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Parse reviews into individual entries
      const reviewLines = reviews.split("\n").filter((line) => line.trim());
      const reviewsData = reviewLines.map((text, index) => ({
        text: text.trim(),
        reviewer_data: {
          id: `reviewer_${index + 1}`,
          account_age_days: Math.floor(Math.random() * 1000) + 30,
          review_count: Math.floor(Math.random() * 100) + 1,
          profile_photo: Math.random() > 0.3,
          verified_email: Math.random() > 0.4,
          verified_phone: Math.random() > 0.6,
        },
        location_data: {
          id: "sample_location",
          name: "Sample Restaurant",
        },
        timestamp: new Date(
          Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000
        ).toISOString(),
      }));

      const result = await eelService.analyzeBulkReviews(reviewsData);

      if (result.success) {
        setResults(result);
      } else {
        setError(result.error || "Failed to analyse reviews");
      }
    } catch (err) {
      setError("Error analysing reviews");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const loadSampleData = () => {
    setReviews(sampleReviews);
  };

  const getTrustColor = (score) => {
    if (score >= 0.7) return "text-green-600";
    if (score >= 0.4) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Bulk Review Analysis
        </h2>
        <p className="text-gray-600">
          Analyse multiple reviews simultaneously to detect patterns and
          anomalies
        </p>
      </div>

      {/* Input Section */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <FileText className="h-5 w-5 mr-2 text-primary-600" />
          Review Input
        </h3>

        <div className="space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Reviews (one per line)
              </label>
              <button
                onClick={loadSampleData}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                Load Sample Data
              </button>
            </div>
            <textarea
              value={reviews}
              onChange={(e) => setReviews(e.target.value)}
              placeholder="Enter reviews separated by line breaks..."
              className="w-full h-40 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <p className="text-sm text-gray-500 mt-1">
              {reviews.split("\n").filter((line) => line.trim()).length} reviews
              entered
            </p>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing || !reviews.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Analysing Reviews...
              </>
            ) : (
              <>
                <BarChart3 className="h-4 w-4 mr-2" />
                Analyse All Reviews
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
      {results && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <div className="flex items-center">
                <FileText className="h-8 w-8 text-blue-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-blue-600">
                    Total Reviews
                  </p>
                  <p className="text-2xl font-bold text-blue-900">
                    {results.summary.total_reviews}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-green-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-green-600">
                    Trusted Reviews
                  </p>
                  <p className="text-2xl font-bold text-green-900">
                    {results.summary.trusted_reviews}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-red-50 to-red-100 border-red-200">
              <div className="flex items-center">
                <AlertTriangle className="h-8 w-8 text-red-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-red-600">
                    Suspicious Reviews
                  </p>
                  <p className="text-2xl font-bold text-red-900">
                    {results.summary.suspicious_reviews}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-purple-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-purple-600">
                    Location Trust
                  </p>
                  <p className="text-2xl font-bold text-purple-900">
                    {(results.location_trust_score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Trust Trend Chart */}
          {results.trust_trends && results.trust_trends.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">
                Trust Score Timeline
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={results.trust_trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) =>
                      new Date(value).toLocaleDateString()
                    }
                  />
                  <YAxis
                    domain={[0, 1]}
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                  />
                  <Tooltip
                    labelFormatter={(value) =>
                      new Date(value).toLocaleDateString()
                    }
                    formatter={(value) => [
                      `${(value * 100).toFixed(1)}%`,
                      "Trust Score",
                    ]}
                  />
                  <Line
                    type="monotone"
                    dataKey="trust_score"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={{ fill: "#3b82f6", strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Anomalies Detection */}
          {results.anomalies && results.anomalies.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold mb-4 text-red-700">
                Detected Anomalies
              </h3>
              <div className="space-y-3">
                {results.anomalies.map((anomaly, index) => (
                  <div
                    key={index}
                    className="p-4 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-red-800 capitalize">
                          {anomaly.anomaly_type.replace("_", " ")}
                        </h4>
                        <p className="text-sm text-red-600 mt-1">
                          Detected on{" "}
                          {new Date(anomaly.timestamp).toLocaleDateString()}
                        </p>
                        {anomaly.review_count && (
                          <p className="text-sm text-red-600">
                            {anomaly.review_count} reviews involved
                          </p>
                        )}
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-medium text-red-700">
                          Severity: {(anomaly.severity * 100).toFixed(0)}%
                        </span>
                        <div className="w-16 h-2 bg-red-200 rounded mt-1">
                          <div
                            className="h-full bg-red-500 rounded"
                            style={{ width: `${anomaly.severity * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Individual Review Results */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">
              Individual Review Analysis
            </h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {results.individual_results.map((result, index) => (
                <div
                  key={index}
                  className="p-3 border border-gray-200 rounded-lg"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span
                      className={`text-sm font-semibold ${getTrustColor(
                        result.trust_score
                      )}`}
                    >
                      Trust Score: {(result.trust_score * 100).toFixed(1)}%
                    </span>
                    <span className="text-xs text-gray-500">
                      Review #{index + 1}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2 line-clamp-2">
                    {reviews.split("\n")[index]?.trim()}
                  </p>
                  <div className="flex space-x-4 text-xs text-gray-500">
                    <span>
                      Authenticity:{" "}
                      {(result.authenticity_score * 100).toFixed(0)}%
                    </span>
                    <span>
                      Fake Risk: {(result.fake_probability * 100).toFixed(0)}%
                    </span>
                    <span>
                      Sentiment:{" "}
                      {result.sentiment_score.overall_score > 0
                        ? "Positive"
                        : "Negative"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BulkAnalyzer;
