"""
Test Runner for Mental Health Pattern Recognition Assistant

This script runs the tests for the Mental Health Pattern Recognition Assistant.
"""

import os
import sys
import unittest
import argparse

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_app import (
    TestDataCollection,
    TestMoodTracking,
    TestPatternRecognition,
    TestCorrelationAnalysis,
    TestVisualization,
    TestIntegration
)

def run_tests(test_type=None, verbose=False):
    """
    Run the specified tests.
    
    Args:
        test_type: Type of tests to run (unit, integration, or all)
        verbose: Whether to show verbose output
    """
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add tests based on type
    if test_type == "unit" or test_type == "all":
        print("Running unit tests...")
        suite.addTest(unittest.makeSuite(TestDataCollection))
        suite.addTest(unittest.makeSuite(TestMoodTracking))
        suite.addTest(unittest.makeSuite(TestPatternRecognition))
        suite.addTest(unittest.makeSuite(TestCorrelationAnalysis))
        suite.addTest(unittest.makeSuite(TestVisualization))
    
    if test_type == "integration" or test_type == "all":
        print("Running integration tests...")
        suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Run tests for Mental Health Pattern Recognition Assistant")
    parser.add_argument("--type", choices=["unit", "integration", "all"], default="all",
                       help="Type of tests to run (unit, integration, or all)")
    parser.add_argument("--verbose", action="store_true", help="Show verbose output")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Mental Health Pattern Recognition Assistant - Test Runner")
    print("=" * 80)
    
    success = run_tests(args.type, args.verbose)
    
    if success:
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
