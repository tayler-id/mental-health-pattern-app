"""
Test Module for Mental Health Pattern Recognition Assistant

This module contains tests for the various components of the Mental Health Pattern Recognition Assistant.
"""

import os
import sys
import unittest
import tempfile
import shutil
import datetime
import json
import random
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector
from src.mood_tracking import MoodTracker
from src.pattern_recognition import PatternRecognitionEngine
from src.correlation_analysis import CorrelationAnalyzer
from src.visualization import VisualizationGenerator

# Import test helpers to add missing methods
from tests.test_helpers import *


class TestDataCollection(unittest.TestCase):
    """Test cases for the DataCollector class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_collector = DataCollector(data_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_record_mood(self):
        """Test recording mood entries."""
        # Record a mood entry
        entry = self.data_collector.record_mood(
            mood_level=7,
            notes="Test mood entry",
            emotions=["happy", "relaxed"]
        )
        
        # Verify entry was recorded
        self.assertIsNotNone(entry)
        self.assertEqual(entry["mood_level"], 7)
        self.assertEqual(entry["notes"], "Test mood entry")
        self.assertEqual(entry["emotions"], ["happy", "relaxed"])
        self.assertIn("timestamp", entry)
        
        # Verify entry was saved
        entries = self.data_collector.get_all_entries("mood_entries")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["mood_level"], 7)
    
    def test_record_activity(self):
        """Test recording activity entries."""
        # Record an activity entry
        entry = self.data_collector.record_activity(
            activity_type="exercise",
            duration_minutes=30,
            intensity=4,
            notes="Test activity entry"
        )
        
        # Verify entry was recorded
        self.assertIsNotNone(entry)
        self.assertEqual(entry["activity_type"], "exercise")
        self.assertEqual(entry["duration_minutes"], 30)
        self.assertEqual(entry["intensity"], 4)
        self.assertEqual(entry["notes"], "Test activity entry")
        self.assertIn("timestamp", entry)
        
        # Verify entry was saved
        entries = self.data_collector.get_all_entries("activity_entries")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["activity_type"], "exercise")
    
    def test_record_sleep(self):
        """Test recording sleep entries."""
        # Record a sleep entry
        entry = self.data_collector.record_sleep(
            duration_hours=7.5,
            quality=8,
            notes="Test sleep entry"
        )
        
        # Verify entry was recorded
        self.assertIsNotNone(entry)
        self.assertEqual(entry["duration_hours"], 7.5)
        self.assertEqual(entry["quality"], 8)
        self.assertEqual(entry["notes"], "Test sleep entry")
        self.assertIn("timestamp", entry)
        
        # Verify entry was saved
        entries = self.data_collector.get_all_entries("sleep_entries")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["duration_hours"], 7.5)
    
    def test_get_entries_by_date_range(self):
        """Test retrieving entries by date range."""
        # Create entries with different dates
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        two_days_ago = now - datetime.timedelta(days=2)
        
        self.data_collector.record_mood(
            mood_level=7,
            timestamp=now.isoformat()
        )
        
        self.data_collector.record_mood(
            mood_level=6,
            timestamp=yesterday.isoformat()
        )
        
        self.data_collector.record_mood(
            mood_level=5,
            timestamp=two_days_ago.isoformat()
        )
        
        # Test retrieving entries from last day
        entries = self.data_collector.get_entries_by_date_range(
            "mood_entries",
            start_date=yesterday.isoformat(),
            end_date=now.isoformat()
        )
        
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["mood_level"], 7)
        self.assertEqual(entries[1]["mood_level"], 6)
        
        # Test retrieving entries from specific date
        entries = self.data_collector.get_entries_by_date_range(
            "mood_entries",
            start_date=two_days_ago.isoformat(),
            end_date=two_days_ago.isoformat()
        )
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["mood_level"], 5)


class TestMoodTracking(unittest.TestCase):
    """Test cases for the MoodTracker class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_collector = DataCollector(data_dir=self.temp_dir)
        self.mood_tracker = MoodTracker(data_collector=self.data_collector)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_log_mood(self):
        """Test logging mood."""
        # Log a mood
        entry = self.mood_tracker.log_mood(
            mood_level=8,
            notes="Test mood log",
            emotions=["happy", "excited"]
        )
        
        # Verify entry was logged
        self.assertIsNotNone(entry)
        self.assertEqual(entry["mood_level"], 8)
        self.assertEqual(entry["notes"], "Test mood log")
        self.assertEqual(entry["emotions"], ["happy", "excited"])
        self.assertIn("timestamp", entry)
        
        # Verify entry was saved
        entries = self.data_collector.get_all_entries("mood_entries")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["mood_level"], 8)
    
    def test_get_mood_history(self):
        """Test retrieving mood history."""
        # Create mood entries
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        two_days_ago = now - datetime.timedelta(days=2)
        
        self.mood_tracker.log_mood(
            mood_level=8,
            timestamp=now.isoformat()
        )
        
        self.mood_tracker.log_mood(
            mood_level=7,
            timestamp=yesterday.isoformat()
        )
        
        self.mood_tracker.log_mood(
            mood_level=6,
            timestamp=two_days_ago.isoformat()
        )
        
        # Test retrieving mood history
        history = self.mood_tracker.get_mood_history(days=2)
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["mood_level"], 8)
        self.assertEqual(history[1]["mood_level"], 7)
    
    def test_calculate_mood_statistics(self):
        """Test calculating mood statistics."""
        # Create mood entries
        self.mood_tracker.log_mood(mood_level=8)
        self.mood_tracker.log_mood(mood_level=6)
        self.mood_tracker.log_mood(mood_level=7)
        
        # Calculate statistics
        stats = self.mood_tracker.calculate_mood_statistics(days=30)
        
        # Verify statistics
        self.assertEqual(stats["average_mood"], 7.0)
        self.assertEqual(stats["mood_range"], (6, 8))
        self.assertIn("mood_volatility", stats)


class TestPatternRecognition(unittest.TestCase):
    """Test cases for the PatternRecognitionEngine class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_collector = DataCollector(data_dir=self.temp_dir)
        self.pattern_engine = PatternRecognitionEngine(data_collector=self.data_collector)
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_data(self):
        """Create test data for pattern recognition."""
        # Create data for the past 30 days
        end_date = datetime.datetime.now()
        
        # Create weekly pattern (better mood on weekends)
        for i in range(30):
            # Create a date i days ago
            date = end_date - datetime.timedelta(days=i)
            
            # Create weekly cycle in mood (better on weekends)
            is_weekend = date.weekday() >= 5
            base_mood = 7 if is_weekend else 5
            
            # Add some random variation
            mood = max(1, min(10, base_mood + random.randint(-1, 2)))
            
            # Record mood
            self.data_collector.record_mood(
                mood_level=mood,
                notes=f"Test mood entry for {date.strftime('%Y-%m-%d')}",
                emotions=["happy"] if mood > 6 else ["neutral"] if mood > 4 else ["sad"],
                timestamp=date.replace(hour=12).isoformat()
            )
            
            # Add exercise every 3 days
            if i % 3 == 0:
                self.data_collector.record_activity(
                    activity_type="exercise",
                    duration_minutes=30,
                    intensity=4,
                    notes="Test exercise entry",
                    timestamp=date.replace(hour=18).isoformat()
                )
            
            # Add sleep entries
            sleep_duration = 8 if is_weekend else 6.5
            self.data_collector.record_sleep(
                duration_hours=sleep_duration,
                quality=7 if sleep_duration >= 7.5 else 5,
                notes="Test sleep record",
                timestamp=date.replace(hour=7).isoformat()
            )
    
    def test_identify_mood_patterns(self):
        """Test identifying mood patterns."""
        # Identify patterns
        patterns = self.pattern_engine.identify_mood_patterns()
        
        # Verify patterns were identified
        self.assertEqual(patterns["status"], "success")
        self.assertIn("time_of_day", patterns)
        self.assertIn("day_of_week", patterns)
        self.assertIn("insights", patterns)
        
        # Verify day of week patterns
        day_of_week = patterns["day_of_week"]
        self.assertIn("weekday", day_of_week)
        self.assertIn("weekend", day_of_week)
        self.assertIn("better_period", day_of_week)
        
        # Weekend mood should be better than weekday mood
        self.assertGreater(day_of_week["weekend"], day_of_week["weekday"])
        self.assertEqual(day_of_week["better_period"], "weekends")


class TestCorrelationAnalysis(unittest.TestCase):
    """Test cases for the CorrelationAnalyzer class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_collector = DataCollector(data_dir=self.temp_dir)
        self.correlation_analyzer = CorrelationAnalyzer(data_collector=self.data_collector)
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_data(self):
        """Create test data for correlation analysis."""
        # Create data for the past 30 days
        end_date = datetime.datetime.now()
        
        # Create patterns with correlations
        for i in range(30):
            # Create a date i days ago
            date = end_date - datetime.timedelta(days=i)
            
            # Exercise improves mood the next day
            exercise_day = (i % 3 == 0)
            
            # Base mood depends on previous day's exercise
            if i > 0 and (i-1) % 3 == 0:
                base_mood = 7  # Day after exercise
            else:
                base_mood = 5  # Regular day
            
            # Add some random variation
            mood = max(1, min(10, base_mood + random.randint(-1, 2)))
            
            # Record mood
            self.data_collector.record_mood(
                mood_level=mood,
                notes=f"Test mood entry for {date.strftime('%Y-%m-%d')}",
                emotions=["happy"] if mood > 6 else ["neutral"] if mood > 4 else ["sad"],
                timestamp=date.replace(hour=12).isoformat()
            )
            
            # Record exercise
            if exercise_day:
                self.data_collector.record_activity(
                    activity_type="exercise",
                    duration_minutes=30,
                    intensity=4,
                    notes="Test exercise entry",
                    timestamp=date.replace(hour=18).isoformat()
                )
            
            # Sleep quality affects mood same day
            sleep_quality = 8 if i % 4 == 0 else 5
            self.data_collector.record_sleep(
                duration_hours=7,
                quality=sleep_quality,
                notes="Test sleep record",
                timestamp=date.replace(hour=7).isoformat()
            )
    
    def test_analyze_activity_mood_correlation(self):
        """Test analyzing activity-mood correlation."""
        # Analyze correlation
        correlation = self.correlation_analyzer.analyze_activity_mood_correlation()
        
        # Verify correlation was analyzed
        self.assertEqual(correlation["status"], "success")
        self.assertIn("correlations", correlation)
        
        # Verify exercise correlation
        exercise_correlation = None
        for corr in correlation["correlations"]:
            if corr["activity_type"] == "exercise":
                exercise_correlation = corr
                break
        
        self.assertIsNotNone(exercise_correlation)
        self.assertIn("correlation", exercise_correlation)
        self.assertIn("lag_correlations", exercise_correlation)
    
    def test_analyze_sleep_mood_correlation(self):
        """Test analyzing sleep-mood correlation."""
        # Analyze correlation
        correlation = self.correlation_analyzer.analyze_sleep_mood_correlation()
        
        # Verify correlation was analyzed
        self.assertEqual(correlation["status"], "success")
        self.assertIn("duration_correlation", correlation)
        self.assertIn("quality_correlation", correlation)
        
        # Quality correlation should be stronger than duration correlation
        self.assertGreater(abs(correlation["quality_correlation"]), 
                          abs(correlation["duration_correlation"]))
    
    def test_generate_comprehensive_correlation_analysis(self):
        """Test generating comprehensive correlation analysis."""
        # Generate analysis
        analysis = self.correlation_analyzer.generate_comprehensive_correlation_analysis()
        
        # Verify analysis was generated
        self.assertIn("lagged_correlations", analysis)
        self.assertIn("granger_causality", analysis)
        self.assertIn("mood_cycles", analysis)
        self.assertIn("key_insights", analysis)


class TestVisualization(unittest.TestCase):
    """Test cases for the VisualizationGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, "visualization")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.data_collector = DataCollector(data_dir=self.temp_dir)
        self.visualization_generator = VisualizationGenerator(
            data_collector=self.data_collector,
            output_dir=self.output_dir
        )
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_data(self):
        """Create test data for visualization."""
        # Create data for the past 30 days
        end_date = datetime.datetime.now()
        
        for i in range(30):
            # Create a date i days ago
            date = end_date - datetime.timedelta(days=i)
            
            # Create mood entry
            mood = random.randint(3, 8)
            self.data_collector.record_mood(
                mood_level=mood,
                notes=f"Test mood entry for {date.strftime('%Y-%m-%d')}",
                emotions=["happy"] if mood > 6 else ["neutral"] if mood > 4 else ["sad"],
                timestamp=date.replace(hour=12).isoformat()
            )
            
            # Create activity entry
            if i % 3 == 0:
                self.data_collector.record_activity(
                    activity_type="exercise",
                    duration_minutes=30,
                    intensity=4,
                    notes="Test exercise entry",
                    timestamp=date.replace(hour=18).isoformat()
                )
            
            # Create sleep entry
            self.data_collector.record_sleep(
                duration_hours=7,
                quality=6,
                notes="Test sleep record",
                timestamp=date.replace(hour=7).isoformat()
            )
    
    def test_generate_mood_timeline(self):
        """Test generating mood timeline visualization."""
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_timeline()
        
        # Verify visualization was generated
        self.assertTrue(os.path.exists(viz_path))
        self.assertTrue(os.path.getsize(viz_path) > 0)
    
    def test_generate_mood_by_day_of_week(self):
        """Test generating mood by day of week visualization."""
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_by_day_of_week()
        
        # Verify visualization was generated
        self.assertTrue(os.path.exists(viz_path))
        self.assertTrue(os.path.getsize(viz_path) > 0)
    
    def test_generate_mood_activity_correlation(self):
        """Test generating mood-activity correlation visualization."""
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_activity_correlation()
        
        # Verify visualization was generated
        self.assertTrue(os.path.exists(viz_path))
        self.assertTrue(os.path.getsize(viz_path) > 0)
    
    def test_generate_mood_sleep_correlation(self):
        """Test generating mood-sleep correlation visualization."""
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_sleep_correlation()
        
        # Verify visualization was generated
        self.assertTrue(os.path.exists(viz_path))
        self.assertTrue(os.path.getsize(viz_path) > 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the Mental Health Pattern Recognition Assistant."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, "visualization")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize components
        self.data_collector = DataCollector(data_dir=self.temp_dir)
        self.mood_tracker = MoodTracker(data_collector=self.data_collector)
        self.pattern_engine = PatternRecognitionEngine(data_collector=self.data_collector)
        self.correlation_analyzer = CorrelationAnalyzer(data_collector=self.data_collector)
        self.visualization_generator = VisualizationGenerator(
            data_collector=self.data_collector,
            output_dir=self.output_dir
        )
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_data(self):
        """Create test data for integration tests."""
        # Create data for the past 60 days
        end_date = datetime.datetime.now()
        
        # Create weekly pattern (better mood on weekends)
        for i in range(60):
            # Create a date i days ago
            date = end_date - datetime.timedelta(days=i)
            
            # Create weekly cycle in mood (better on weekends)
            is_weekend = date.weekday() >= 5
            base_mood = 7 if is_weekend else 5
            
            # Add some random variation
            mood = max(1, min(10, base_mood + random.randint(-1, 2)))
            
            # Record mood
            self.data_collector.record_mood(
                mood_level=mood,
                notes=f"Test mood entry for {date.strftime('%Y-%m-%d')}",
                emotions=["happy"] if mood > 6 else ["neutral"] if mood > 4 else ["sad"],
                timestamp=date.replace(hour=12).isoformat()
            )
            
            # Add exercise every 3 days, which improves mood the next day
            if i % 3 == 0:
                self.data_collector.record_activity(
                    activity_type="exercise",
                    duration_minutes=30,
                    intensity=4,
                    notes="Test exercise entry",
                    timestamp=date.replace(hour=18).isoformat()
                )
                
                # Mood is better the day after exercise
                if i > 0:
                    next_day = date + datetime.timedelta(days=1)
                    next_day_mood = min(10, mood + 2)
                    
                    self.data_collector.record_mood(
                        mood_level=next_day_mood,
                        notes="Day after exercise",
                        emotions=["energetic", "positive"],
                        timestamp=next_day.replace(hour=12).isoformat()
                    )
            
            # Add sleep entries with a pattern (better sleep on weekends)
            sleep_duration = 8 if is_weekend else 6.5
            self.data_collector.record_sleep(
                duration_hours=sleep_duration,
                quality=7 if sleep_duration >= 7.5 else 5,
                notes="Test sleep record",
                timestamp=date.replace(hour=7).isoformat()
            )
    
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow."""
        # 1. Record a new mood entry
        mood_entry = self.mood_tracker.log_mood(
            mood_level=8,
            notes="Integration test mood entry",
            emotions=["happy", "relaxed"]
        )
        
        self.assertIsNotNone(mood_entry)
        
        # 2. Get mood history
        history = self.mood_tracker.get_mood_history(days=30)
        self.assertGreater(len(history), 0)
        
        # 3. Identify patterns
        patterns = self.pattern_engine.identify_mood_patterns()
        self.assertEqual(patterns["status"], "success")
        
        # 4. Analyze correlations
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis()
        self.assertIn("lagged_correlations", correlations)
        
        # 5. Generate visualizations
        timeline_path = self.visualization_generator.generate_mood_timeline()
        self.assertTrue(os.path.exists(timeline_path))
        
        # 6. Generate dashboard
        dashboard_path = self.visualization_generator.generate_dashboard()
        self.assertTrue(os.path.exists(dashboard_path))
        
        # 7. Verify all components work together
        summary = self.mood_tracker.generate_mood_summary()
        self.assertEqual(summary["status"], "success")
        self.assertIn("statistics", summary)
        self.assertIn("emotions", summary)
        self.assertIn("insights", summary)


if __name__ == "__main__":
    unittest.main()
