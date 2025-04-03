"""
Python Bridge Script for Node.js Integration
This script acts as a bridge between Node.js and the Mental Health Pattern Recognition data collection module.
"""

import sys
import json
import os
import traceback
from datetime import datetime

# Adjust Python's path to properly find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from src.data_collection import DataCollector

    # Get command line arguments
    if len(sys.argv) < 5:
        print(json.dumps({
            "success": False,
            "error": "Insufficient arguments. Required: mood_level, notes, emotions_json, streak"
        }))
        sys.exit(1)

    # Parse arguments
    mood_level = int(sys.argv[1])
    notes = sys.argv[2]
    emotions_json = sys.argv[3]
    streak = int(sys.argv[4])
    
    # Initialize data collector with proper path
    collector = DataCollector(data_dir='data')
    
    # Parse emotions from JSON
    emotions = json.loads(emotions_json)
    
    # Record mood data
    entry = collector.record_mood(
        mood_level=mood_level,
        notes=notes,
        emotions=emotions
    )
    
    # Add streak information to the response
    result = {
        "success": True,
        "mood_entry": entry,
        "streak": streak,
        "timestamp": datetime.now().isoformat()
    }
    
    # Return success response
    print(json.dumps(result))
    
except Exception as e:
    # Return error response
    print(json.dumps({
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc() if 'traceback' in sys.modules else "Traceback not available"
    }))
    sys.exit(1)
