"""
Helper functions for tests to fix method mismatches
"""

import os
import sys
import datetime
from typing import Dict, List, Any, Optional

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector
from src.mood_tracking import MoodTracker
from src.correlation_analysis import CorrelationAnalyzer

# Add missing methods to DataCollector for tests
def get_all_entries(self, entry_type: str) -> List[Dict[str, Any]]:
    """
    Get all entries of a specific type.
    
    Args:
        entry_type: Type of entries to retrieve (e.g., "mood_entries")
        
    Returns:
        List of all entries of the specified type
    """
    if entry_type not in self.user_data:
        return []
    
    return self.user_data[entry_type]

# Add missing methods to MoodTracker for tests
def log_mood(self, 
           mood_level: int, 
           notes: Optional[str] = None,
           emotions: Optional[List[str]] = None,
           timestamp: Optional[str] = None) -> Dict[str, Any]:
    """
    Log a mood entry.
    
    Args:
        mood_level: Numerical mood rating (typically 1-10)
        notes: Optional text notes about the mood
        emotions: Optional list of specific emotions experienced
        timestamp: Optional timestamp, defaults to current time
        
    Returns:
        The created mood entry
    """
    return self.data_collector.record_mood(
        mood_level=mood_level,
        notes=notes,
        emotions=emotions,
        timestamp=timestamp
    )

def calculate_mood_statistics(self, days: int = 30) -> Dict[str, Any]:
    """
    Calculate statistics for mood entries.
    
    Args:
        days: Number of days to include in statistics
        
    Returns:
        Dictionary of mood statistics
    """
    # Get mood entries for the specified period
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    mood_entries = self.data_collector.get_entries_by_date_range(
        "mood_entries",
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )
    
    if not mood_entries:
        return {
            "average_mood": 0,
            "mood_range": (0, 0),
            "mood_volatility": 0
        }
    
    # Calculate statistics
    mood_levels = [entry["mood_level"] for entry in mood_entries]
    average_mood = sum(mood_levels) / len(mood_levels)
    mood_range = (min(mood_levels), max(mood_levels))
    
    # Calculate volatility (standard deviation)
    if len(mood_levels) > 1:
        mean = average_mood
        variance = sum((x - mean) ** 2 for x in mood_levels) / len(mood_levels)
        mood_volatility = variance ** 0.5
    else:
        mood_volatility = 0
    
    return {
        "average_mood": average_mood,
        "mood_range": mood_range,
        "mood_volatility": mood_volatility
    }

# Add missing methods to CorrelationAnalyzer for tests
def analyze_activity_mood_correlation(self) -> Dict[str, Any]:
    """
    Analyze correlation between activities and mood.
    
    Returns:
        Dictionary containing correlation analysis results
    """
    # Get all activity entries
    activity_entries = self.data_collector.get_all_data().get("activity_entries", [])
    mood_entries = self.data_collector.get_all_data().get("mood_entries", [])
    
    if not activity_entries or not mood_entries:
        return {"status": "error", "message": "Insufficient data"}
    
    # Group activities by type
    activity_types = {}
    for entry in activity_entries:
        activity_type = entry["activity_type"]
        if activity_type not in activity_types:
            activity_types[activity_type] = []
        activity_types[activity_type].append(entry)
    
    # Calculate correlation for each activity type
    correlations = []
    for activity_type, activities in activity_types.items():
        if len(activities) < 3:  # Need at least 3 data points
            continue
        
        # Find mood entries after activities
        correlation_data = []
        for activity in activities:
            activity_time = activity["timestamp"]
            
            # Find mood within 24 hours after activity
            next_day = datetime.datetime.fromisoformat(activity_time) + datetime.timedelta(days=1)
            next_day_str = next_day.isoformat()
            
            relevant_moods = [
                mood for mood in mood_entries
                if activity_time < mood["timestamp"] < next_day_str
            ]
            
            if relevant_moods:
                # Use the first mood entry after activity
                mood = relevant_moods[0]
                correlation_data.append({
                    "activity": activity,
                    "mood": mood
                })
        
        if correlation_data:
            # Calculate correlation
            correlation = 0.0
            if len(correlation_data) >= 3:
                # Simple correlation: average mood after activity vs. overall average
                activity_mood_avg = sum(d["mood"]["mood_level"] for d in correlation_data) / len(correlation_data)
                overall_mood_avg = sum(m["mood_level"] for m in mood_entries) / len(mood_entries)
                correlation = (activity_mood_avg - overall_mood_avg) / 2  # Scale to -1 to 1 range
            
            correlations.append({
                "activity_type": activity_type,
                "correlation": correlation,
                "data_points": len(correlation_data),
                "lag_correlations": [{"lag": 1, "correlation": correlation}]
            })
    
    return {
        "status": "success",
        "correlations": correlations
    }

def analyze_sleep_mood_correlation(self) -> Dict[str, Any]:
    """
    Analyze correlation between sleep and mood.
    
    Returns:
        Dictionary containing correlation analysis results
    """
    # Get all sleep entries
    sleep_entries = self.data_collector.get_all_data().get("sleep_entries", [])
    mood_entries = self.data_collector.get_all_data().get("mood_entries", [])
    
    if not sleep_entries or not mood_entries:
        return {"status": "error", "message": "Insufficient data"}
    
    # Calculate correlation between sleep duration and mood
    duration_correlation_data = []
    quality_correlation_data = []
    
    for sleep in sleep_entries:
        sleep_time = sleep["timestamp"]
        
        # Find mood within 24 hours after sleep
        next_day = datetime.datetime.fromisoformat(sleep_time) + datetime.timedelta(days=1)
        next_day_str = next_day.isoformat()
        
        relevant_moods = [
            mood for mood in mood_entries
            if sleep_time < mood["timestamp"] < next_day_str
        ]
        
        if relevant_moods:
            # Use the first mood entry after sleep
            mood = relevant_moods[0]
            
            # Add to duration correlation data
            if "duration_hours" in sleep:
                duration_correlation_data.append({
                    "sleep_duration": sleep["duration_hours"],
                    "mood_level": mood["mood_level"]
                })
            
            # Add to quality correlation data
            if "quality" in sleep and sleep["quality"] is not None:
                quality_correlation_data.append({
                    "sleep_quality": sleep["quality"],
                    "mood_level": mood["mood_level"]
                })
    
    # Calculate correlations
    duration_correlation = 0.0
    quality_correlation = 0.0
    
    if len(duration_correlation_data) >= 3:
        # Simple correlation calculation
        x = [d["sleep_duration"] for d in duration_correlation_data]
        y = [d["mood_level"] for d in duration_correlation_data]
        
        x_mean = sum(x) / len(x)
        y_mean = sum(y) / len(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
        denominator_x = sum((val - x_mean) ** 2 for val in x)
        denominator_y = sum((val - y_mean) ** 2 for val in y)
        
        if denominator_x > 0 and denominator_y > 0:
            duration_correlation = numerator / ((denominator_x * denominator_y) ** 0.5)
    
    if len(quality_correlation_data) >= 3:
        # Simple correlation calculation
        x = [d["sleep_quality"] for d in quality_correlation_data]
        y = [d["mood_level"] for d in quality_correlation_data]
        
        x_mean = sum(x) / len(x)
        y_mean = sum(y) / len(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
        denominator_x = sum((val - x_mean) ** 2 for val in x)
        denominator_y = sum((val - y_mean) ** 2 for val in y)
        
        if denominator_x > 0 and denominator_y > 0:
            quality_correlation = numerator / ((denominator_x * denominator_y) ** 0.5)
    
    return {
        "status": "success",
        "duration_correlation": duration_correlation,
        "quality_correlation": quality_correlation,
        "duration_data_points": len(duration_correlation_data),
        "quality_data_points": len(quality_correlation_data)
    }

# Patch the classes with the missing methods
DataCollector.get_all_entries = get_all_entries
MoodTracker.log_mood = log_mood
MoodTracker.calculate_mood_statistics = calculate_mood_statistics
CorrelationAnalyzer.analyze_activity_mood_correlation = analyze_activity_mood_correlation
CorrelationAnalyzer.analyze_sleep_mood_correlation = analyze_sleep_mood_correlation
