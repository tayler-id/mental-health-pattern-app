"""
Data Collection Module for Mental Health Pattern Recognition Assistant

This module handles the collection and storage of mood, activities, and other relevant
data points for pattern analysis.
"""

import json
import datetime
import os
from typing import Dict, List, Any, Optional, Union

class DataCollector:
    """
    Handles collection and storage of mental health-related data points.
    """
    
    def __init__(self, data_dir: str = "../data"):
        """
        Initialize the data collector with a directory for data storage.
        
        Args:
            data_dir: Directory path where data will be stored
        """
        self.data_dir = data_dir
        self.ensure_data_directory()
        self.user_data_file = os.path.join(data_dir, "user_data.json")
        self.load_existing_data()
    
    def ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_existing_data(self) -> None:
        """Load existing user data if available, or initialize empty data structure."""
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    self.user_data = json.load(f)
            except json.JSONDecodeError:
                # Handle corrupted data file
                self.initialize_empty_data()
        else:
            self.initialize_empty_data()
    
    def initialize_empty_data(self) -> None:
        """Initialize an empty data structure for a new user."""
        self.user_data = {
            "mood_entries": [],
            "activity_entries": [],
            "sleep_entries": [],
            "medication_entries": [],
            "custom_entries": [],
            "user_settings": {
                "tracking_categories": ["mood", "activities", "sleep"],
                "mood_scale": {
                    "min": 1,
                    "max": 10,
                    "labels": {
                        "1": "Very Poor",
                        "5": "Neutral",
                        "10": "Excellent"
                    }
                },
                "notification_preferences": {
                    "enabled": True,
                    "frequency": "daily",
                    "time": "20:00"
                }
            }
        }
    
    def save_data(self) -> None:
        """Save current user data to file."""
        with open(self.user_data_file, 'w') as f:
            json.dump(self.user_data, f, indent=2)
    
    def record_mood(self, 
                   mood_level: int, 
                   notes: Optional[str] = None,
                   emotions: Optional[List[str]] = None,
                   timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a mood entry.
        
        Args:
            mood_level: Numerical mood rating (typically 1-10)
            notes: Optional text notes about the mood
            emotions: Optional list of specific emotions experienced
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            The created mood entry
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        entry = {
            "timestamp": timestamp,
            "mood_level": mood_level,
            "notes": notes,
            "emotions": emotions or []
        }
        
        self.user_data["mood_entries"].append(entry)
        self.save_data()
        return entry
    
    def record_activity(self,
                       activity_type: str,
                       duration_minutes: Optional[int] = None,
                       intensity: Optional[int] = None,
                       notes: Optional[str] = None,
                       timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Record an activity entry.
        
        Args:
            activity_type: Type of activity (e.g., "exercise", "social", "work")
            duration_minutes: Optional duration in minutes
            intensity: Optional intensity rating (typically 1-5)
            notes: Optional text notes about the activity
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            The created activity entry
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        entry = {
            "timestamp": timestamp,
            "activity_type": activity_type,
            "duration_minutes": duration_minutes,
            "intensity": intensity,
            "notes": notes
        }
        
        self.user_data["activity_entries"].append(entry)
        self.save_data()
        return entry
    
    def record_sleep(self,
                    duration_hours: float,
                    quality: Optional[int] = None,
                    start_time: Optional[str] = None,
                    end_time: Optional[str] = None,
                    notes: Optional[str] = None,
                    timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a sleep entry.
        
        Args:
            duration_hours: Sleep duration in hours
            quality: Optional sleep quality rating (typically 1-10)
            start_time: Optional sleep start time
            end_time: Optional sleep end time
            notes: Optional text notes about sleep
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            The created sleep entry
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        entry = {
            "timestamp": timestamp,
            "duration_hours": duration_hours,
            "quality": quality,
            "start_time": start_time,
            "end_time": end_time,
            "notes": notes
        }
        
        self.user_data["sleep_entries"].append(entry)
        self.save_data()
        return entry
    
    def record_medication(self,
                         medication_name: str,
                         dosage: Optional[str] = None,
                         taken: bool = True,
                         notes: Optional[str] = None,
                         timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a medication entry.
        
        Args:
            medication_name: Name of medication
            dosage: Optional dosage information
            taken: Whether medication was taken
            notes: Optional text notes
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            The created medication entry
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        entry = {
            "timestamp": timestamp,
            "medication_name": medication_name,
            "dosage": dosage,
            "taken": taken,
            "notes": notes
        }
        
        self.user_data["medication_entries"].append(entry)
        self.save_data()
        return entry
    
    def record_custom_entry(self,
                           category: str,
                           values: Dict[str, Any],
                           timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a custom entry for user-defined tracking categories.
        
        Args:
            category: Custom category name
            values: Dictionary of values to record
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            The created custom entry
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        entry = {
            "timestamp": timestamp,
            "category": category,
            "values": values
        }
        
        self.user_data["custom_entries"].append(entry)
        self.save_data()
        return entry
    
    def get_entries_by_date_range(self, 
                                 entry_type: str,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve entries of a specific type within a date range.
        
        Args:
            entry_type: Type of entries to retrieve (e.g., "mood_entries")
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            List of entries within the specified date range
        """
        if entry_type not in self.user_data:
            return []
        
        entries = self.user_data[entry_type]
        
        if start_date is None and end_date is None:
            return entries
        
        filtered_entries = []
        for entry in entries:
            entry_date = entry["timestamp"]
            
            if start_date and entry_date < start_date:
                continue
                
            if end_date and entry_date > end_date:
                continue
                
            filtered_entries.append(entry)
            
        return filtered_entries
    
    def get_all_data(self) -> Dict[str, Any]:
        """
        Get all user data.
        
        Returns:
            Complete user data dictionary
        """
        return self.user_data
    
    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user settings.
        
        Args:
            settings: Dictionary of settings to update
            
        Returns:
            Updated settings dictionary
        """
        self.user_data["user_settings"].update(settings)
        self.save_data()
        return self.user_data["user_settings"]
    
    def export_data(self, format_type: str = "json") -> str:
        """
        Export user data in specified format.
        
        Args:
            format_type: Format for export (currently only "json" supported)
            
        Returns:
            Path to exported file
        """
        if format_type.lower() == "json":
            export_path = os.path.join(self.data_dir, "exported_data.json")
            with open(export_path, 'w') as f:
                json.dump(self.user_data, f, indent=2)
            return export_path
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def import_data(self, import_path: str) -> bool:
        """
        Import user data from a file.
        
        Args:
            import_path: Path to file to import
            
        Returns:
            True if import was successful, False otherwise
        """
        try:
            with open(import_path, 'r') as f:
                imported_data = json.load(f)
            
            # Validate imported data structure
            required_keys = ["mood_entries", "activity_entries", "user_settings"]
            if not all(key in imported_data for key in required_keys):
                return False
            
            # Backup current data before overwriting
            backup_path = os.path.join(self.data_dir, f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(backup_path, 'w') as f:
                json.dump(self.user_data, f)
            
            # Update with imported data
            self.user_data = imported_data
            self.save_data()
            return True
            
        except (json.JSONDecodeError, FileNotFoundError):
            return False


# Example usage
if __name__ == "__main__":
    collector = DataCollector()
    
    # Record a mood entry
    collector.record_mood(
        mood_level=7, 
        notes="Feeling pretty good today", 
        emotions=["happy", "calm"]
    )
    
    # Record an activity
    collector.record_activity(
        activity_type="exercise",
        duration_minutes=30,
        intensity=4,
        notes="Morning jog"
    )
    
    # Get recent mood entries
    recent_moods = collector.get_entries_by_date_range("mood_entries")
    print(f"Recorded {len(recent_moods)} mood entries")
