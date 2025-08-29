# TikTok Hackathon 2025 - Review Trust System

## 🎯 Project Overview

**Theme:** "Filtering the noise: ML for trustworthy location reviews"

This application uses advanced machine learning techniques to analyse and score the trustworthiness of location reviews, helping users identify authentic feedback and filter out fake or manipulated content.

## 🌟 Features

### Core ML Features

- **Review Authenticity Scoring** - Multi-factor analysis using NLP and behavioral patterns
- **Fake Review Detection** - Graph neural networks and pattern recognition
- **Sentiment Consistency Analysis** - Cross-validation of emotional authenticity
- **Temporal Anomaly Detection** - Identify review bombing and coordinated campaigns
- **Multi-Modal Verification** - Text and image content verification
- **Reviewer Credibility Profiling** - Comprehensive trust scoring for reviewers

### User Interface Features

- **Single Review Analyzer** - Instant analysis of individual reviews
- **Bulk Review Analysis** - Process multiple reviews for location-wide insights
- **Trust Dashboard** - Comprehensive visualization of trust metrics and trends
- **Reviewer Profile Analysis** - Deep dive into reviewer behavior and credibility
- **Real-time Risk Assessment** - Live monitoring of trust factors and anomalies

## 🛠 Technology Stack

### Backend (Python)

- **Python-Eel** - Bridge between Python backend and web frontend
- **scikit-learn** - Machine learning algorithms
- **TextBlob & NLTK** - Natural language processing
- **Transformers** - Advanced NLP models (BERT, RoBERTa)
- **NumPy & Pandas** - Data processing and analysis

### Frontend

The current repository contains the Python backend, services, and tests. A UI can be added later; for now, focus is on ML services and a robust test suite.

### ML Models & Techniques

- **Ensemble Trust Scoring** - Combining multiple ML approaches
- **Temporal Pattern Analysis** - Time-series anomaly detection
- **Network Analysis** - Reviewer relationship mapping
- **Sentiment Analysis** - Multi-dimensional emotional assessment
- **Linguistic Feature Extraction** - Advanced text analysis

## 📊 Analysis Components

### 1. Review Authenticity Analysis

- Linguistic pattern recognition
- Sentiment consistency checking
- Content quality assessment
- Spam and bot detection

### 2. Reviewer Behavior Analysis

- Account age and activity patterns
- Review frequency analysis
- Profile completeness scoring
- Cross-platform validation

### 3. Network Analysis

- Reviewer relationship mapping
- Coordinated behavior detection
- IP clustering analysis
- Social proof validation

### 4. Temporal Analysis

- Review timing patterns
- Velocity anomaly detection
- Seasonal trend analysis
- Campaign identification

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone and setup:**

   ```bash
   git clone <repository>
   cd tiktok-hackathon-2025
   ```

2. **Manual setup (if script fails):**

   ```bash
   # Backend setup
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # No frontend in this repo
   ```

3. **Run the tests:**

   ```bash
   # Activate virtual environment
   source venv/bin/activate

   # Run all unit tests
   python -m unittest -q
   ```

The services are designed as importable classes and functions; integrate them into a UI or API as needed.

## 📱 Usage Guide

### Single Review Analysis

1. Navigate to the "Single Review" tab
2. Enter the review text
3. Optionally add reviewer information (account age, review count, verification status)
4. Click "Analyze Review" to get comprehensive trust metrics

### Bulk Analysis

1. Go to the "Bulk Analysis" tab
2. Enter multiple reviews (one per line) or load sample data
3. Click "Analyze All Reviews" to process the entire dataset
4. View location-wide trust metrics, trends, and anomaly detection

### Trust Dashboard

1. Select "Trust Dashboard" to view location-level analytics
2. Choose different locations from the dropdown
3. Explore trust trends, risk factors, and review distributions
4. Review flagged content and highly trusted reviews

### Reviewer Profiles

1. Access "Reviewer Profile" tab
2. Enter a reviewer ID or use sample profiles
3. View comprehensive credibility analysis
4. Explore behavioral patterns and trust factors

## 🎯 ML Model Details

### Trust Score Calculation

The trust score combines multiple factors:

- **Authenticity Score (25%)** - Linguistic and behavioral authenticity
- **Sentiment Quality (20%)** - Emotional consistency and naturalness
- **Reviewer Credibility (25%)** - Account history and verification
- **Content Quality (15%)** - Information density and specificity
- **Temporal Consistency (15%)** - Review timing patterns

### Fake Review Detection

Uses ensemble methods including:

- Pattern recognition for common fake review templates
- Behavioral analysis of reviewer activity
- Network analysis for coordinated campaigns
- Temporal anomaly detection for review bombing

### Risk Assessment

Multi-dimensional risk evaluation:

- Text pattern analysis
- Account age and activity risks
- Review frequency anomalies
- Profile completeness assessment

## 📈 Sample Outputs

### Trust Score Categories

- **Highly Trusted (80-100%)** - Strong authenticity indicators
- **Trusted (60-79%)** - Good credibility with minor concerns
- **Moderate Trust (40-59%)** - Mixed signals, use with caution
- **Low Trust (20-39%)** - Multiple suspicious patterns
- **Untrusted (0-19%)** - High probability of fake content

### Detected Anomalies

- Review bombing campaigns
- Coordinated fake review networks
- Temporal posting irregularities
- Sentiment manipulation patterns

## 🔧 Development

### Project Structure

```text
tiktok-hackathon-2025/
├── backend/
│   ├── services/              # ML analysis services
│   │   ├── review_analyser.py
│   │   ├── sentiment_analyser.py
│   │   ├── fake_detector.py
│   │   └── trust_scorer.py
│   └── utils/                 # Utility functions
│       └── data_processor.py
├── tests/                     # Unit tests (unittest)
│   ├── services/
│   └── utils/
└── README.md
```

### Adding New Features

1. Add new ML services to `backend/services/`
2. Add utilities to `backend/utils/`
3. Extend tests in `tests/` to cover new behaviour

## 🧪 Testing

- Run all tests: `python -m unittest -q`
- Focus a file: `python -m unittest tests/services/test_sentiment_analyser.py -q`
- Tests use British English naming (Analyser, Behaviour, etc.).

## 🏆 Hackathon Highlights

### Innovation

- **Multi-Modal Analysis** - Combines text, behavioral, and temporal signals
- **Real-time Processing** - Instant analysis with visual feedback
- **Explainable AI** - Clear reasoning for trust scores
- **Scalable Architecture** - Designed for high-volume review analysis

### Impact

- Helps consumers identify trustworthy reviews
- Enables businesses to monitor review authenticity
- Reduces influence of fake review campaigns
- Improves overall review ecosystem quality

## 🤝 Contributing

This project was built for the TikTok Hackathon 2025. The code demonstrates advanced ML techniques for review trust analysis and serves as a foundation for production-scale review verification systems.

## 📄 License

MIT License - Built for TikTok Hackathon 2025

---

**Team:** Filtering the Noise  
**Theme:** ML for Trustworthy Location Reviews  
**Tech Stack:** Python (TextBlob, scikit-learn, NumPy)  
**Year:** 2025
