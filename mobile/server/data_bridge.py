"""
Data Bridge Script for Node.js Integration
This script retrieves mood data from the Mental Health Pattern Recognition data collection module.
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
    
    # Expect command, days, page, per_page as arguments
    if len(sys.argv) < 4:
        print(json.dumps({
            "success": False,
            "error": "Insufficient arguments. Required: command, days, page, per_page"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    days = int(sys.argv[2])
    page = int(sys.argv[3])
    per_page = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    # Initialize data collector with proper path
    collector = DataCollector(data_dir='data')
    
    if command == 'get_mood_data':
        # Calculate date range based on days
        end_date = datetime.now().isoformat()
        # We don't need to calculate start_date as the get_entries_by_date_range function
        # will filter based on the days parameter
        
        # Get mood entries
        all_entries = collector.get_entries_by_date_range('mood_entries')
        
        # Sort by timestamp (newest first)
        all_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_entries = all_entries[start_idx:end_idx]
        
        # Prepare response
        result = {
            "success": True,
            "data": {
                "entries": paginated_entries,
                "pagination": {
                    "total": len(all_entries),
                    "page": page,
                    "per_page": per_page,
                    "total_pages": (len(all_entries) + per_page - 1) // per_page
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        print(json.dumps(result))
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
