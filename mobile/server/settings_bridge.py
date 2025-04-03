"""
Settings Bridge Script for Node.js Integration
This script connects to the DataCollector to manage user settings.
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
    
    # Expect command and potentially settings JSON as arguments
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Insufficient arguments. Required: command[, settings_json]"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Initialize data collector with proper path
    collector = DataCollector(data_dir='data')
    
    # Process command
    if command == 'get_settings':
        # Get current settings
        user_data = collector.get_all_data()
        settings = user_data.get("user_settings", {})
        
        # Add metadata to response
        response = {
            "success": True,
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "settings": settings
        }
        
        print(json.dumps(response))
    
    elif command == 'update_settings':
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "error": "Missing settings JSON parameter for update operation"
            }))
            sys.exit(1)
        
        # Parse settings JSON
        settings_json = sys.argv[2]
        settings = json.loads(settings_json)
        
        # Update settings
        updated_settings = collector.update_settings(settings)
        
        # Add metadata to response
        response = {
            "success": True,
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "settings": updated_settings
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
