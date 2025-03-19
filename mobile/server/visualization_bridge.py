"""
Visualization Bridge Script for Node.js Integration
This script connects to the Visualization Generator to create visualizations of mental health data.
"""

import sys
import json
import os
import traceback
import base64
from datetime import datetime

# Adjust Python's path to properly find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from src.visualization import VisualizationGenerator
    from src.data_collection import DataCollector
    from src.pattern_recognition import PatternRecognitionEngine
    
    # Expect command, visualization_type, days as arguments
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Insufficient arguments. Required: command, visualization_type, days"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    viz_type = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    # Initialize components
    collector = DataCollector(data_dir='data')
    viz_generator = VisualizationGenerator(collector, output_dir='visualization')
    
    # Create visualization output directory if it doesn't exist
    viz_dir = os.path.join('visualization', 'api_output')
    os.makedirs(viz_dir, exist_ok=True)
    
    # Function to encode image to base64 for direct embedding in responses
    def encode_image(image_path):
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    
    # Generate visualization based on type
    if command == 'generate_visualization':
        image_path = None
        
        if viz_type == 'mood_timeline':
            image_path = viz_generator.generate_mood_timeline(
                days=days, 
                save_path=os.path.join(viz_dir, f'mood_timeline_{days}days.png')
            )
            
        elif viz_type == 'mood_by_day':
            image_path = viz_generator.generate_mood_by_day_of_week(
                days=days, 
                save_path=os.path.join(viz_dir, f'mood_by_day_{days}days.png')
            )
            
        elif viz_type == 'mood_activity':
            # Check if specific activity type was provided
            activity_type = sys.argv[4] if len(sys.argv) > 4 else None
            
            image_path = viz_generator.generate_mood_activity_correlation(
                activity_type=activity_type,
                days=days, 
                save_path=os.path.join(viz_dir, f'mood_activity_{days}days.png')
            )
            
        elif viz_type == 'mood_sleep':
            image_path = viz_generator.generate_mood_sleep_correlation(
                days=days, 
                save_path=os.path.join(viz_dir, f'mood_sleep_{days}days.png')
            )
            
        elif viz_type == 'emotion_distribution':
            image_path = viz_generator.generate_emotion_distribution(
                days=days, 
                save_path=os.path.join(viz_dir, f'emotion_dist_{days}days.png')
            )
            
        elif viz_type == 'pattern_visualization':
            # Run pattern recognition first
            pattern_engine = PatternRecognitionEngine(collector)
            patterns = pattern_engine.identify_mood_patterns(days=days)
            
            image_path = viz_generator.generate_pattern_visualization(
                pattern_data=patterns,
                days=days, 
                save_path=os.path.join(viz_dir, f'patterns_{days}days.png')
            )
            
        elif viz_type == 'dashboard':
            image_path = viz_generator.generate_dashboard(
                days=days, 
                save_path=os.path.join(viz_dir, f'dashboard_{days}days.png')
            )
            
        else:
            print(json.dumps({
                "success": False,
                "error": f"Unknown visualization type: {viz_type}"
            }))
            sys.exit(1)
            
        # Encode the image to base64 for direct embedding
        base64_image = encode_image(image_path)
        
        # Prepare response
        response = {
            "success": True,
            "visualization_type": viz_type,
            "days": days,
            "timestamp": datetime.now().isoformat(),
            "image_path": image_path,
            "image_base64": base64_image
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
