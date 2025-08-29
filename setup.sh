#!/bin/bash

echo "🚀 Setting up TikTok Hackathon 2025 - Review Trust System"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "🐍 Detected Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and essential tools first
echo "⬆️ Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install packages one by one to handle errors better
echo "📚 Installing core dependencies..."

echo "Installing eel..."
pip install "eel>=0.16.0"

echo "Installing numpy..."
pip install "numpy>=1.26.0"

echo "Installing pandas..."
pip install "pandas>=2.1.0"

echo "Installing scikit-learn..."
pip install "scikit-learn>=1.4.0"

echo "Installing textblob..."
pip install "textblob>=0.17.1"

echo "Installing nltk..."
pip install "nltk>=3.8.1"

echo "Installing other dependencies..."
pip install "requests>=2.31.0"
pip install "python-dateutil>=2.8.2"

# Optional packages (install if possible, but don't fail if they don't work)
echo "📊 Installing optional visualization packages..."
pip install "matplotlib>=3.8.0" || echo "⚠️ matplotlib installation failed - continuing without it"
pip install "seaborn>=0.13.0" || echo "⚠️ seaborn installation failed - continuing without it"
pip install "plotly>=5.17.0" || echo "⚠️ plotly installation failed - continuing without it"

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    print('✅ NLTK data downloaded successfully')
except Exception as e:
    print(f'⚠️ NLTK data download failed: {e}')
"

# Install frontend dependencies
echo "⚛️ Installing frontend dependencies..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "1. source venv/bin/activate"
echo "2. python main.py"
echo ""
echo "The application will open at http://localhost:8080"
