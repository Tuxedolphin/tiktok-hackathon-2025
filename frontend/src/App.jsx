import React, { useState, Suspense, lazy } from "react";
import { Shield, TrendingUp, Users, AlertTriangle } from "lucide-react";
const ReviewAnalyzer = lazy(() => import("./components/ReviewAnalyzer"));
const TrustDashboard = lazy(() => import("./components/TrustDashboard"));
const BulkAnalyzer = lazy(() => import("./components/BulkAnalyzer"));
const ReviewerProfile = lazy(() => import("./components/ReviewerProfile"));

function App() {
  const [currentTab, setCurrentTab] = useState("analyzer");

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Shield className="h-8 w-8 text-primary-600" />
              <h1 className="text-xl font-bold text-gray-900">
                Review Trust System
              </h1>
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                TikTok Hackathon 2025
              </span>
            </div>

            <nav className="flex space-x-4">
              <button
                onClick={() => setCurrentTab("analyzer")}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentTab === "analyzer"
                    ? "bg-primary-100 text-primary-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <Shield className="h-4 w-4 inline mr-2" />
                Single Review
              </button>

              <button
                onClick={() => setCurrentTab("bulk")}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentTab === "bulk"
                    ? "bg-primary-100 text-primary-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <TrendingUp className="h-4 w-4 inline mr-2" />
                Bulk Analysis
              </button>

              <button
                onClick={() => setCurrentTab("dashboard")}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentTab === "dashboard"
                    ? "bg-primary-100 text-primary-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <AlertTriangle className="h-4 w-4 inline mr-2" />
                Trust Dashboard
              </button>

              <button
                onClick={() => setCurrentTab("reviewer")}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentTab === "reviewer"
                    ? "bg-primary-100 text-primary-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <Users className="h-4 w-4 inline mr-2" />
                Reviewer Profile
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Suspense fallback={<div className="text-center">Loading...</div>}>
          {currentTab === "analyzer" && <ReviewAnalyzer />}
          {currentTab === "bulk" && <BulkAnalyzer />}
          {currentTab === "dashboard" && <TrustDashboard />}
          {currentTab === "reviewer" && <ReviewerProfile />}
        </Suspense>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>
              TikTok Hackathon 2025 - Filtering the noise: ML for trustworthy
              location reviews
            </p>
            <p className="mt-1">
              Built with Python-Eel, React, and Machine Learning
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
