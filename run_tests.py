#!/usr/bin/env python3
"""
Test runner for the TikTok Hackathon 2025 backend test suite.

This script discovers and runs all unit tests in the tests/ directory.
"""

import os
import sys
import unittest
from typing import Optional


def run_tests(test_pattern: str = "test_*.py", verbosity: int = 2) -> bool:
    """
    Discover and run all tests matching the pattern.

    Args:
        test_pattern: Pattern to match test files (default: "test_*.py")
        verbosity: Test output verbosity level (default: 2)

    Returns:
        True if all tests passed, False otherwise
    """
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Add the project root to Python path so we can import backend modules
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Change to the tests directory
    tests_dir = os.path.join(project_root, "tests")
    os.chdir(tests_dir)

    # Discover tests
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=".", pattern=test_pattern, top_level_dir=tests_dir
    )

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_specific_test(
    test_module: str,
    test_class: Optional[str] = None,
    test_method: Optional[str] = None,
    verbosity: int = 2,
) -> bool:
    """
    Run a specific test module, class, or method.

    Args:
        test_module: Name of the test module (e.g., "services.test_review_analyzer")
        test_class: Optional test class name
        test_method: Optional test method name
        verbosity: Test output verbosity level

    Returns:
        True if all tests passed, False otherwise
    """
    # Get the project root directory and add to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Build the test target
    test_target = f"tests.{test_module}"
    if test_class:
        test_target += f".{test_class}"
        if test_method:
            test_target += f".{test_method}"

    # Load and run the specific test
    suite = unittest.TestLoader().loadTestsFromName(test_target)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result.wasSuccessful()


def main() -> int:
    """Main entry point for the test runner."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run TikTok Hackathon 2025 backend tests"
    )
    parser.add_argument(
        "--pattern",
        "-p",
        default="test_*.py",
        help="Pattern to match test files (default: test_*.py)",
    )
    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        choices=[0, 1, 2],
        default=2,
        help="Test output verbosity (0=quiet, 1=normal, 2=verbose)",
    )
    parser.add_argument(
        "--module",
        "-m",
        help="Run specific test module (e.g., services.test_review_analyzer)",
    )
    parser.add_argument(
        "--class",
        "-c",
        dest="test_class",
        help="Run specific test class (requires --module)",
    )
    parser.add_argument(
        "--method",
        "-t",
        dest="test_method",
        help="Run specific test method (requires --module and --class)",
    )

    args = parser.parse_args()

    print("TikTok Hackathon 2025 - Backend Test Suite")
    print("=" * 50)

    if args.module:
        # Run specific test
        if args.test_method and not args.test_class:
            print("Error: --method requires --class to be specified")
            return 1

        print(f"Running specific test: {args.module}")
        if args.test_class:
            print(f"  Class: {args.test_class}")
        if args.test_method:
            print(f"  Method: {args.test_method}")
        print()

        success = run_specific_test(
            args.module, args.test_class, args.test_method, args.verbosity
        )
    else:
        # Run all tests
        print(f"Running all tests matching pattern: {args.pattern}")
        print()
        success = run_tests(args.pattern, args.verbosity)

    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
