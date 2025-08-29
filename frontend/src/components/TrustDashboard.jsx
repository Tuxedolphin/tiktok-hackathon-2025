import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { TrendingUp, AlertTriangle, Users, Star } from "lucide-react";
import eelService from "../services/eel";

const TrustDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLocation, setSelectedLocation] = useState("location_123");

  useEffect(() => {
    // Call loader without adding as dependency to avoid re-creating function
    (async () => {
      setLoading(true);
      try {
        const result = await eelService.getTrustDashboardData(selectedLocation);
        if (result.success) {
          setDashboardData(result);
        }
      } catch (error) {
        console.error("Error loading dashboard data:", error);
      } finally {
        setLoading(false);
      }
    })();
  }, [selectedLocation]);

  // Manual refresh function can be re-added if needed

  const trustDistributionData = dashboardData
    ? [
        {
          name: "High Trust",
          value: dashboardData.trust_distribution.high_trust,
          color: "#10b981",
        },
        {
          name: "Medium Trust",
          value: dashboardData.trust_distribution.medium_trust,
          color: "#f59e0b",
        },
        {
          name: "Low Trust",
          value: dashboardData.trust_distribution.low_trust,
          color: "#ef4444",
        },
      ]
    : [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span className="ml-2">Loading dashboard data...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Trust Dashboard
        </h2>
        <p className="text-gray-600">
          Comprehensive trust analytics and monitoring for location reviews
        </p>
      </div>

      {/* Location Selector */}
      <div className="card">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Location Analysis</h3>
          <select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="location_123">The Great Restaurant</option>
            <option value="location_456">Amazing Cafe</option>
            <option value="location_789">Perfect Bistro</option>
          </select>
        </div>
      </div>

      {dashboardData && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card bg-gradient-to-br from-primary-50 to-primary-100 border-primary-200">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <TrendingUp className="h-8 w-8 text-primary-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-primary-600">
                    Overall Trust Score
                  </p>
                  <p className="text-2xl font-bold text-primary-900">
                    {(dashboardData.overall_trust_score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Users className="h-8 w-8 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-green-600">
                    Total Reviews
                  </p>
                  <p className="text-2xl font-bold text-green-900">
                    {dashboardData.total_reviews.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-yellow-50 to-yellow-100 border-yellow-200">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <AlertTriangle className="h-8 w-8 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-yellow-600">
                    Risk Level
                  </p>
                  <p className="text-2xl font-bold text-yellow-900">
                    {dashboardData.risk_factors.fake_review_probability > 0.3
                      ? "High"
                      : dashboardData.risk_factors.fake_review_probability >
                        0.15
                      ? "Medium"
                      : "Low"}
                  </p>
                </div>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Star className="h-8 w-8 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-purple-600">
                    Trust Trend
                  </p>
                  <p className="text-2xl font-bold text-purple-900">
                    {dashboardData.trend_data &&
                    dashboardData.trend_data.length > 1 &&
                    dashboardData.trend_data[
                      dashboardData.trend_data.length - 1
                    ].trust_score >
                      dashboardData.trend_data[
                        dashboardData.trend_data.length - 2
                      ].trust_score
                      ? "↗️"
                      : "↘️"}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Trust Score Trend */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">
                Trust Score Trend (30 Days)
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={dashboardData.trend_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
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

            {/* Trust Distribution */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Trust Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={trustDistributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) =>
                      `${name}: ${(percent * 100).toFixed(0)}%`
                    }
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {trustDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Reviews Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Trusted Reviews */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4 text-green-700">
                Most Trusted Reviews
              </h3>
              <div className="space-y-3">
                {dashboardData.top_trusted_reviews.map((review) => (
                  <div
                    key={review.id}
                    className="p-3 bg-green-50 border border-green-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-medium text-green-800">
                        Trust Score: {(review.trust_score * 100).toFixed(1)}%
                      </span>
                      <span className="text-xs text-green-600">
                        {review.date}
                      </span>
                    </div>
                    <p className="text-sm text-green-700 line-clamp-2">
                      {review.text}
                    </p>
                    <div className="flex items-center mt-2">
                      <div className="flex">
                        {[...Array(review.rating)].map((_, i) => (
                          <Star
                            key={i}
                            className="h-3 w-3 fill-current text-yellow-400"
                          />
                        ))}
                      </div>
                      <span className="ml-2 text-xs text-green-600">
                        {review.rating}/5 stars
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Flagged Reviews */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4 text-red-700">
                Flagged Reviews
              </h3>
              <div className="space-y-3">
                {dashboardData.flagged_reviews.map((review) => (
                  <div
                    key={review.id}
                    className="p-3 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-medium text-red-800">
                        Trust Score: {(review.trust_score * 100).toFixed(1)}%
                      </span>
                      <span className="text-xs text-red-600">
                        {review.date}
                      </span>
                    </div>
                    <p className="text-sm text-red-700 line-clamp-2">
                      {review.text}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {review.flags.map((flag, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 text-xs bg-red-200 text-red-800 rounded"
                        >
                          {flag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Risk Factors */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Risk Assessment</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    Fake Review Probability
                  </span>
                  <span
                    className={`text-sm font-bold ${
                      dashboardData.risk_factors.fake_review_probability > 0.3
                        ? "text-red-600"
                        : dashboardData.risk_factors.fake_review_probability >
                          0.15
                        ? "text-yellow-600"
                        : "text-green-600"
                    }`}
                  >
                    {(
                      dashboardData.risk_factors.fake_review_probability * 100
                    ).toFixed(1)}
                    %
                  </span>
                </div>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      dashboardData.risk_factors.fake_review_probability > 0.3
                        ? "bg-red-500"
                        : dashboardData.risk_factors.fake_review_probability >
                          0.15
                        ? "bg-yellow-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${
                        dashboardData.risk_factors.fake_review_probability * 100
                      }%`,
                    }}
                  />
                </div>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    Network Anomalies
                  </span>
                  <span className="text-sm font-bold text-gray-900">
                    {dashboardData.risk_factors.reviewer_network_anomalies}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Suspicious reviewer connections detected
                </p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    Temporal Anomalies
                  </span>
                  <span className="text-sm font-bold text-gray-900">
                    {dashboardData.risk_factors.temporal_anomalies}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Unusual timing patterns found
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default TrustDashboard;
