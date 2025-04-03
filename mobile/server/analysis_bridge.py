"""
Analysis Bridge Script for Node.js Integration
This script connects to the Pattern Recognition Engine to analyze mental health data.
"""

import sys
import json
import os
import traceback
from datetime import datetime

# Adjust Python's path to properly find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from src.pattern_recognition import PatternRecognitionEngine
    from src.data_collection import DataCollector
    
    # Expect command, analysis_type, days as arguments
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Insufficient arguments. Required: command, analysis_type, days"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    analysis_type = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    # Initialize pattern recognition engine
    collector = DataCollector(data_dir='data')
    engine = PatternRecognitionEngine(collector)
    
    # Choose analysis based on command
    if command == 'analyze_patterns':
        if analysis_type == 'mood':
            result = engine.identify_mood_patterns(days)
        elif analysis_type == 'activity':
            result = engine.identify_activity_mood_correlations(days)
        elif analysis_type == 'sleep':
            result = engine.identify_sleep_mood_correlations(days)
        elif analysis_type == 'clusters':
            result = engine.identify_mood_clusters(days)
        elif analysis_type == 'comprehensive':
            result = engine.generate_comprehensive_analysis(days)
        else:
            print(json.dumps({
                "success": False,
                "error": f"Unknown analysis type: {analysis_type}"
            }))
            sys.exit(1)
            
        # Add metadata
        response = {
            "success": True,
            "analysis_type": analysis_type,
            "days": days,
            "timestamp": datetime.now().isoformat(),
            "data": result
        }
        
        print(json.dumps(response))
    else:
        print(json.dumps({
            "success": False,
            "error": f"Unknown command: {command}"
        }))
        sys.exit(1)
    
except Exception as e:
    print(json.dumps({
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc()
    }))
    sys.exit(1)
