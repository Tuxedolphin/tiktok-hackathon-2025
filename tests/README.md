# Test Suite Documentation

This directory contains comprehensive unit tests for the TikTok Hackathon 2025 backend services.

## Directory Structure

```
tests/
├── __init__.py                         # Test package initialisation
├── test_config.py                      # Centralised test configuration and sample data
├── services/                           # Tests for backend services
│   ├── __init__.py
│   ├── test_review_analyser.py         # Tests for ReviewAnalyser
│   ├── test_sentiment_analyser.py      # Tests for SentimentAnalyser
│   ├── test_fake_detector.py          # Tests for FakeReviewDetector
│   └── test_trust_scorer.py           # Tests for TrustScorer
└── utils/                              # Tests for utility modules
    ├── __init__.py
    └── test_data_processor.py          # Tests for DataProcessor
```

## Running Tests

### Using the Test Runner

The project includes a comprehensive test runner (`run_tests.py`) with various options:

```bash
# Run all tests
python run_tests.py

# Run with quiet output
python run_tests.py --verbosity 0

# Run tests matching a specific pattern
python run_tests.py --pattern "test_review*.py"

# Run a specific test module
python run_tests.py --module services.test_review_analyser

# Run a specific test class
python run_tests.py --module services.test_review_analyser --class TestReviewAnalyser

# Run a specific test method
python run_tests.py --module services.test_review_analyser --class TestReviewAnalyser --method test_calculate_authenticity_score
```

### Using unittest directly

```bash
# Run all tests
python -m unittest discover tests

# Run tests in a specific directory
python -m unittest discover tests/services

# Run a specific test file
python -m unittest tests.services.test_review_analyser

# Run a specific test class
python -m unittest tests.services.test_review_analyser.TestReviewAnalyser

# Run a specific test method
python -m unittest tests.services.test_review_analyser.TestReviewAnalyser.test_calculate_authenticity_score
```

## Test Coverage

### Services Tests

#### ReviewAnalyser (`test_review_analyser.py`)

- ✅ Initialisation and configuration
- ✅ Authenticity score calculation with various inputs
- ✅ Authenticity factors analysis
- ✅ Edge cases (empty reviews, invalid data)
- ✅ Error handling for malformed input

#### SentimentAnalyser (`test_sentiment_analyser.py`)

- ✅ Initialisation and TextBlob integration
- ✅ Sentiment polarity analysis
- ✅ Subjectivity measurement
- ✅ Sentiment manipulation detection
- ✅ Edge cases and error handling

#### FakeReviewDetector (`test_fake_detector.py`)

- ✅ Fake review detection algorithms
- ✅ Temporal anomaly detection
- ✅ Reviewer behaviour analysis
- ✅ Location-based detection
- ✅ Integration with trust trends

#### TrustScorer (`test_trust_scorer.py`)

- ✅ Trust score calculation
- ✅ Trust categorisation
- ✅ Trust explanation generation
- ✅ Location trust calculation
- ✅ Comprehensive scoring algorithms

### Utils Tests

#### DataProcessor (`test_data_processor.py`)

- ✅ Sample data generation
- ✅ Trend data creation
- ✅ Statistics calculation
- ✅ Data export functionality
- ✅ Reviewer activity simulation

## Test Configuration

The `test_config.py` file provides centralised test data and configuration:

- **SAMPLE_REVIEWS**: Comprehensive set of sample review data
- **SAMPLE_REVIEWER_DATA**: Mock reviewer profiles and metadata
- **get_sample_trust_trends()**: Function to generate test trust trend data

## Test Patterns and Best Practices

### Test Structure

Each test file follows the standard unittest pattern:

- `setUp()` method for test initialisation
- Descriptive test method names starting with `test_`
- Comprehensive assertions using unittest's assertion methods
- Proper teardown and cleanup

### Assertion Patterns

- Type checking: `assertIsInstance()`
- Value validation: `assertEqual()`, `assertGreater()`, `assertIn()`
- Structure validation: checking dictionary keys and list lengths
- Error handling: `assertRaises()` for exception testing

### Mock Testing

- Uses `unittest.mock` for testing error conditions
- Mocks external dependencies and protected methods
- Validates method calls and parameter passing

## Adding New Tests

When adding new functionality, follow these guidelines:

1. **Create test file**: Name it `test_<module_name>.py`
2. **Import dependencies**: Import the module under test and test configuration
3. **Create test class**: Inherit from `unittest.TestCase`
4. **Add setUp method**: Initialize test fixtures
5. **Write test methods**: One test method per functionality
6. **Use descriptive names**: Test method names should describe what they test
7. **Add docstrings**: Document what each test validates
8. **Update this README**: Add new test coverage information

### Example Test Method

```python
def test_new_functionality_with_valid_input(self) -> None:
    """Test that new functionality works correctly with valid input."""
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = self.service.new_functionality(input_data)

    # Assert
    self.assertIsInstance(result, dict)
    self.assertIn("expected_key", result)
    self.assertEqual(result["expected_key"], "expected_value")
```

## Continuous Integration

These tests are designed to be run in CI/CD pipelines:

- All tests are self-contained and don't require external services
- Test data is generated programmatically
- No external file dependencies
- Deterministic results for reliable CI runs

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project root is in PYTHONPATH
2. **Missing Dependencies**: Install required packages (TextBlob, etc.)
3. **Path Issues**: Run tests from the project root directory

### Debug Mode

Run tests with maximum verbosity to see detailed output:

```bash
python run_tests.py --verbosity 2
```

## Performance

The complete test suite typically runs in under 10 seconds, making it suitable for:

- Pre-commit hooks
- Continuous integration
- Development workflow integration
- Quick validation during development
