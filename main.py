"""
Main Application Module for Mental Health Pattern Recognition Assistant

This module integrates all components of the Mental Health Pattern Recognition Assistant
and provides the main entry point for running the application.
"""

import os
import sys
import argparse
from src.data_collection import DataCollector
from src.mood_tracking import MoodTracker
from src.pattern_recognition import PatternRecognitionEngine
from src.correlation_analysis import CorrelationAnalyzer
from src.visualization import VisualizationGenerator
from src.user_interface import UserInterface

def setup_directories(data_dir, output_dir):
    """
    Set up necessary directories for the application.
    
    Args:
        data_dir: Directory for data storage
        output_dir: Directory for visualization output
    """
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories for organization
    os.makedirs(os.path.join(data_dir, "exports"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "mood"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "patterns"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "correlations"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "dashboards"), exist_ok=True)

def main():
    """
    Main function to run the Mental Health Pattern Recognition Assistant.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Mental Health Pattern Recognition Assistant")
    parser.add_argument("--data-dir", default="./data", help="Directory for data storage")
    parser.add_argument("--output-dir", default="./visualization", help="Directory for visualization output")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    
    args = parser.parse_args()
    
    # Set up directories
    setup_directories(args.data_dir, args.output_dir)
    
    # Initialize components
    data_collector = DataCollector(data_dir=args.data_dir)
    mood_tracker = MoodTracker(data_collector=data_collector)
    pattern_engine = PatternRecognitionEngine(data_collector=data_collector)
    correlation_analyzer = CorrelationAnalyzer(data_collector=data_collector)
    visualization_generator = VisualizationGenerator(
        data_collector=data_collector,
        output_dir=args.output_dir
    )
    
    # Load demo data if requested
    if args.demo:
        load_demo_data(data_collector)
    
    # Create and run the user interface
    ui = UserInterface(
        data_dir=args.data_dir,
        output_dir=args.output_dir
    )
    ui.run()

def load_demo_data(data_collector):
    """
    Load demo data for demonstration purposes.
    
    Args:
        data_collector: DataCollector instance to load data into
    """
    import datetime
    import random
    import numpy as np
    
    print("Loading demo data...")
    
    # Generate data for the past 60 days
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
        emotions = []
        if mood >= 8:
            emotions = random.sample(["happy", "content", "excited", "grateful"], k=random.randint(1, 2))
        elif mood >= 6:
            emotions = random.sample(["relaxed", "calm", "content"], k=random.randint(1, 2))
        elif mood >= 4:
            emotions = random.sample(["neutral", "contemplative", "focused"], k=random.randint(1, 2))
        elif mood >= 2:
            emotions = random.sample(["sad", "tired", "anxious"], k=random.randint(1, 2))
        else:
            emotions = random.sample(["depressed", "overwhelmed", "hopeless"], k=random.randint(1, 2))
        
        data_collector.record_mood(
            mood_level=mood,
            notes=f"Demo mood entry for {date.strftime('%Y-%m-%d')}",
            emotions=emotions,
            timestamp=date.replace(hour=12, minute=random.randint(0, 59)).isoformat()
        )
        
        # Add exercise every 3 days, which improves mood the next day
        if i % 3 == 0:
            data_collector.record_activity(
                activity_type="exercise",
                duration_minutes=30 + random.randint(0, 30),
                intensity=random.randint(3, 5),
                notes="Demo exercise entry",
                timestamp=date.replace(hour=18, minute=random.randint(0, 59)).isoformat()
            )
            
            # Mood is better the day after exercise
            if i > 0:
                next_day = date + datetime.timedelta(days=1)
                next_day_mood = min(10, mood + 2)
                
                data_collector.record_mood(
                    mood_level=next_day_mood,
                    notes="Day after exercise",
                    emotions=["energetic", "positive"],
                    timestamp=next_day.replace(hour=12, minute=random.randint(0, 59)).isoformat()
                )
        
        # Add social activity once a week, which also improves mood
        if i % 7 == 2:
            data_collector.record_activity(
                activity_type="social",
                duration_minutes=90 + random.randint(0, 60),
                intensity=random.randint(2, 4),
                notes="Demo social activity entry",
                timestamp=date.replace(hour=19, minute=random.randint(0, 59)).isoformat()
            )
        
        # Add work activity on weekdays
        if not is_weekend:
            data_collector.record_activity(
                activity_type="work",
                duration_minutes=480 + random.randint(-60, 60),
                intensity=random.randint(3, 5),
                notes="Demo work entry",
                timestamp=date.replace(hour=9, minute=random.randint(0, 59)).isoformat()
            )
        
        # Add sleep entries with a pattern (better sleep on weekends)
        sleep_duration = 8 if is_weekend else 6.5
        sleep_duration += random.uniform(-0.5, 0.5)  # Add some variation
        
        data_collector.record_sleep(
            duration_hours=sleep_duration,
            quality=7 if sleep_duration >= 7.5 else 5,
            notes="Demo sleep record",
            start_time=date.replace(hour=23, minute=random.randint(0, 59)).isoformat(),
            end_time=(date + datetime.timedelta(days=1)).replace(hour=7, minute=random.randint(0, 59)).isoformat()
        )
        
        # Add medication entries for a subset of days
        if i % 2 == 0:
            data_collector.record_medication(
                medication_name="Demo Medication",
                dosage="10mg",
                taken=random.random() > 0.1,  # 90% compliance
                notes="Demo medication entry",
                timestamp=date.replace(hour=8, minute=random.randint(0, 59)).isoformat()
            )
    
    print("Demo data loaded successfully!")

if __name__ == "__main__":
    main()
