#!/usr/bin/env python3
"""
Web Bridge Module for Mental Health Pattern Recognition Assistant

This module provides a bridge between the web server and the CLI application,
allowing the web UI to access the functionality of the CLI app.
"""

import sys
import json
import traceback
import datetime
from typing import Dict, List, Any, Optional, Union
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules from the CLI app
from src.data_collection import DataCollector
from src.mood_tracking import MoodTracker
from src.pattern_recognition import PatternRecognitionEngine
from src.correlation_analysis import CorrelationAnalyzer
from src.visualization import VisualizationGenerator

# Initialize the components
data_dir = os.environ.get('DATA_DIR', './data')
output_dir = os.environ.get('OUTPUT_DIR', './visualization')

# Create directories if they don't exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Initialize the components
data_collector = DataCollector(data_dir=data_dir)
mood_tracker = MoodTracker(data_collector=data_collector)
pattern_engine = PatternRecognitionEngine(data_collector=data_collector)
correlation_analyzer = CorrelationAnalyzer(data_collector=data_collector)
visualization_generator = VisualizationGenerator(
    data_collector=data_collector,
    output_dir=output_dir
)

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle a request from the web server.
    
    Args:
        request_data: Dictionary containing the request data
        
    Returns:
        Dictionary containing the response data
    """
    function_name = request_data.get('function')
    params = request_data.get('params', {})
    
    try:
        # Call the appropriate function based on the function name
        if function_name == 'get_all_entries':
            result = get_all_entries(params)
        elif function_name == 'get_entries_by_date_range':
            result = get_entries_by_date_range(params)
        elif function_name == 'get_entry_by_id':
            result = get_entry_by_id(params)
        elif function_name == 'record_mood':
            result = record_mood(params)
        elif function_name == 'update_mood':
            result = update_mood(params)
        elif function_name == 'delete_entry':
            result = delete_entry(params)
        elif function_name == 'get_mood_statistics':
            result = get_mood_statistics(params)
        elif function_name == 'identify_mood_patterns':
            result = identify_mood_patterns(params)
        elif function_name == 'identify_activity_mood_correlations':
            result = identify_activity_mood_correlations(params)
        elif function_name == 'identify_sleep_mood_correlations':
            result = identify_sleep_mood_correlations(params)
        elif function_name == 'generate_comprehensive_analysis':
            result = generate_comprehensive_analysis(params)
        elif function_name == 'generate_mood_timeline':
            result = generate_mood_timeline(params)
        elif function_name == 'get_mood_timeline_data':
            result = get_mood_timeline_data(params)
        elif function_name == 'generate_mood_by_day_of_week':
            result = generate_mood_by_day_of_week(params)
        elif function_name == 'get_mood_by_day_data':
            result = get_mood_by_day_data(params)
        elif function_name == 'generate_emotion_distribution':
            result = generate_emotion_distribution(params)
        elif function_name == 'get_emotion_distribution_data':
            result = get_emotion_distribution_data(params)
        elif function_name == 'generate_mood_activity_correlation':
            result = generate_mood_activity_correlation(params)
        elif function_name == 'get_activity_mood_correlation_data':
            result = get_activity_mood_correlation_data(params)
        elif function_name == 'generate_mood_sleep_correlation':
            result = generate_mood_sleep_correlation(params)
        elif function_name == 'get_sleep_mood_correlation_data':
            result = get_sleep_mood_correlation_data(params)
        elif function_name == 'generate_pattern_visualization':
            result = generate_pattern_visualization(params)
        elif function_name == 'get_pattern_visualization_data':
            result = get_pattern_visualization_data(params)
        elif function_name == 'generate_dashboard':
            result = generate_dashboard(params)
        elif function_name == 'get_dashboard_data':
            result = get_dashboard_data(params)
        elif function_name == 'export_data':
            result = export_data(params)
        elif function_name == 'import_data':
            result = import_data(params)
        else:
            return {
                'error': {
                    'message': f'Unknown function: {function_name}'
                }
            }
        
        return {
            'data': result
        }
    except Exception as e:
        # Return an error response
        traceback.print_exc()
        return {
            'error': {
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        }

# Function implementations

def get_all_entries(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get all entries of a specific type."""
    entry_type = params.get('entry_type')
    return data_collector.user_data.get(entry_type, [])

def get_entries_by_date_range(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get entries by date range."""
    entry_type = params.get('entry_type')
    start_date = params.get('start_date')
    end_date = params.get('end_date')
    
    return data_collector.get_entries_by_date_range(
        entry_type=entry_type,
        start_date=start_date,
        end_date=end_date
    )

def get_entry_by_id(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get entry by ID."""
    entry_type = params.get('entry_type')
    entry_id = params.get('id')
    
    entries = data_collector.user_data.get(entry_type, [])
    for entry in entries:
        if entry.get('id') == entry_id:
            return entry
    
    return None

def record_mood(params: Dict[str, Any]) -> Dict[str, Any]:
    """Record a mood entry."""
    mood_level = params.get('mood_level')
    notes = params.get('notes', '')
    emotions = params.get('emotions', [])
    timestamp = params.get('timestamp')
    
    return data_collector.record_mood(
        mood_level=mood_level,
        notes=notes,
        emotions=emotions,
        timestamp=timestamp
    )

def update_mood(params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a mood entry."""
    entry_id = params.get('id')
    mood_level = params.get('mood_level')
    notes = params.get('notes')
    emotions = params.get('emotions')
    timestamp = params.get('timestamp')
    
    # Find the entry
    entries = data_collector.user_data.get('mood_entries', [])
    for i, entry in enumerate(entries):
        if entry.get('id') == entry_id:
            # Update the entry
            if mood_level is not None:
                entries[i]['mood_level'] = mood_level
            if notes is not None:
                entries[i]['notes'] = notes
            if emotions is not None:
                entries[i]['emotions'] = emotions
            if timestamp is not None:
                entries[i]['timestamp'] = timestamp
            
            # Save the data
            data_collector.save_data()
            
            return entries[i]
    
    raise ValueError(f"Mood entry with ID {entry_id} not found")

def delete_entry(params: Dict[str, Any]) -> bool:
    """Delete an entry."""
    entry_type = params.get('entry_type')
    entry_id = params.get('id')
    
    # Find the entry
    entries = data_collector.user_data.get(entry_type, [])
    for i, entry in enumerate(entries):
        if entry.get('id') == entry_id:
            # Remove the entry
            del entries[i]
            
            # Save the data
            data_collector.save_data()
            
            return True
    
    raise ValueError(f"Entry with ID {entry_id} not found in {entry_type}")

def get_mood_statistics(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get mood statistics."""
    days = params.get('days', 30)
    
    # Get mood entries
    mood_entries = data_collector.get_entries_by_date_range(
        entry_type='mood_entries',
        days=days
    )
    
    if not mood_entries:
        return {
            'average_mood': None,
            'mood_range': None,
            'most_common_emotions': [],
            'entry_count': 0
        }
    
    # Calculate statistics
    mood_levels = [entry.get('mood_level', 0) for entry in mood_entries]
    average_mood = sum(mood_levels) / len(mood_levels)
    mood_range = (min(mood_levels), max(mood_levels))
    
    # Count emotions
    emotion_counts = {}
    for entry in mood_entries:
        for emotion in entry.get('emotions', []):
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Get most common emotions
    most_common_emotions = sorted(
        emotion_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    return {
        'average_mood': average_mood,
        'mood_range': mood_range,
        'most_common_emotions': most_common_emotions,
        'entry_count': len(mood_entries)
    }

def identify_mood_patterns(params: Dict[str, Any]) -> Dict[str, Any]:
    """Identify mood patterns."""
    days = params.get('days', 90)
    return pattern_engine.identify_mood_patterns(days=days)

def identify_activity_mood_correlations(params: Dict[str, Any]) -> Dict[str, Any]:
    """Identify activity-mood correlations."""
    days = params.get('days', 90)
    return pattern_engine.identify_activity_mood_correlations(days=days)

def identify_sleep_mood_correlations(params: Dict[str, Any]) -> Dict[str, Any]:
    """Identify sleep-mood correlations."""
    days = params.get('days', 90)
    return pattern_engine.identify_sleep_mood_correlations(days=days)

def generate_comprehensive_analysis(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive analysis."""
    days = params.get('days', 90)
    return pattern_engine.generate_comprehensive_analysis(days=days)

def generate_mood_timeline(params: Dict[str, Any]) -> str:
    """Generate mood timeline visualization."""
    days = params.get('days', 30)
    return visualization_generator.generate_mood_timeline(days=days)

def get_mood_timeline_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get mood timeline data for client-side visualization."""
    days = params.get('days', 30)
    
    # Get mood entries
    mood_entries = data_collector.get_entries_by_date_range(
        entry_type='mood_entries',
        days=days
    )
    
    # Format data for visualization
    data = []
    for entry in mood_entries:
        data.append({
            'date': entry.get('timestamp'),
            'mood_level': entry.get('mood_level'),
            'emotions': entry.get('emotions', []),
            'notes': entry.get('notes', '')
        })
    
    return {
        'entries': data
    }

def generate_mood_by_day_of_week(params: Dict[str, Any]) -> str:
    """Generate mood by day of week visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_mood_by_day_of_week(days=days)

def get_mood_by_day_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get mood by day of week data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get mood entries
    mood_entries = data_collector.get_entries_by_date_range(
        entry_type='mood_entries',
        days=days
    )
    
    # Group by day of week
    day_mapping = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    
    day_data = {day: [] for day in day_mapping.values()}
    
    for entry in mood_entries:
        timestamp = entry.get('timestamp')
        if timestamp:
            date = datetime.datetime.fromisoformat(timestamp)
            day_name = day_mapping[date.weekday()]
            day_data[day_name].append(entry.get('mood_level', 0))
    
    # Calculate averages
    result = []
    for day, mood_levels in day_data.items():
        if mood_levels:
            average_mood = sum(mood_levels) / len(mood_levels)
        else:
            average_mood = 0
        
        result.append({
            'day': day,
            'average_mood': average_mood,
            'entry_count': len(mood_levels)
        })
    
    return {
        'day_averages': result
    }

def generate_emotion_distribution(params: Dict[str, Any]) -> str:
    """Generate emotion distribution visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_emotion_distribution(days=days)

def get_emotion_distribution_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get emotion distribution data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get mood entries
    mood_entries = data_collector.get_entries_by_date_range(
        entry_type='mood_entries',
        days=days
    )
    
    # Count emotions
    emotion_counts = {}
    for entry in mood_entries:
        for emotion in entry.get('emotions', []):
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Format data for visualization
    data = []
    for emotion, count in emotion_counts.items():
        data.append({
            'emotion': emotion,
            'count': count
        })
    
    # Sort by count
    data.sort(key=lambda x: x['count'], reverse=True)
    
    return {
        'emotions': data
    }

def generate_mood_activity_correlation(params: Dict[str, Any]) -> str:
    """Generate mood-activity correlation visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_mood_activity_correlation(days=days)

def get_activity_mood_correlation_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get activity-mood correlation data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get correlation analysis
    correlations = pattern_engine.identify_activity_mood_correlations(days=days)
    
    if correlations.get('status') != 'success':
        return {
            'correlations': []
        }
    
    return {
        'correlations': correlations.get('correlations', []),
        'insights': correlations.get('insights', [])
    }

def generate_mood_sleep_correlation(params: Dict[str, Any]) -> str:
    """Generate mood-sleep correlation visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_mood_sleep_correlation(days=days)

def get_sleep_mood_correlation_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get sleep-mood correlation data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get correlation analysis
    correlations = pattern_engine.identify_sleep_mood_correlations(days=days)
    
    if correlations.get('status') != 'success':
        return {
            'correlations': []
        }
    
    return {
        'correlations': correlations.get('correlations', []),
        'insights': correlations.get('insights', [])
    }

def generate_pattern_visualization(params: Dict[str, Any]) -> str:
    """Generate pattern visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_pattern_visualization(days=days)

def get_pattern_visualization_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get pattern visualization data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get pattern analysis
    patterns = pattern_engine.identify_mood_patterns(days=days)
    
    if patterns.get('status') != 'success':
        return {
            'patterns': []
        }
    
    return {
        'patterns': patterns.get('patterns', []),
        'insights': patterns.get('insights', [])
    }

def generate_dashboard(params: Dict[str, Any]) -> str:
    """Generate dashboard visualization."""
    days = params.get('days', 90)
    return visualization_generator.generate_dashboard(days=days)

def get_dashboard_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get dashboard data for client-side visualization."""
    days = params.get('days', 90)
    
    # Get all the data needed for the dashboard
    mood_timeline = get_mood_timeline_data({'days': days})
    mood_by_day = get_mood_by_day_data({'days': days})
    emotion_distribution = get_emotion_distribution_data({'days': days})
    activity_correlations = get_activity_mood_correlation_data({'days': days})
    sleep_correlations = get_sleep_mood_correlation_data({'days': days})
    
    return {
        'mood_timeline': mood_timeline,
        'mood_by_day': mood_by_day,
        'emotion_distribution': emotion_distribution,
        'activity_correlations': activity_correlations,
        'sleep_correlations': sleep_correlations
    }

def export_data(params: Dict[str, Any]) -> str:
    """Export data to a file."""
    format_type = params.get('format', 'json')
    return data_collector.export_data(format_type=format_type)

def import_data(params: Dict[str, Any]) -> bool:
    """Import data from a file."""
    file_path = params.get('file_path')
    return data_collector.import_data(import_path=file_path)

def main():
    """Main function to handle requests from stdin."""
    # Read input from stdin
    input_data = sys.stdin.read()
    
    try:
        # Parse the input as JSON
        request_data = json.loads(input_data)
        
        # Handle the request
        response_data = handle_request(request_data)
        
        # Write the response to stdout
        json.dump(response_data, sys.stdout, cls=JSONEncoder)
    except json.JSONDecodeError:
        # Handle invalid JSON input
        error_response = {
            'error': {
                'message': 'Invalid JSON input'
            }
        }
        json.dump(error_response, sys.stdout)
    except Exception as e:
        # Handle unexpected errors
        error_response = {
            'error': {
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        }
        json.dump(error_response, sys.stdout)

if __name__ == '__main__':
    main()
