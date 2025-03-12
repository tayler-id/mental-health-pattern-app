"""
User Interface Module for Mental Health Pattern Recognition Assistant

This module provides a command-line interface for interacting with the Mental Health
Pattern Recognition Assistant, allowing users to input data, view visualizations,
and receive insights about their mental health patterns.
"""

import os
import sys
import datetime
import argparse
import time
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
from tabulate import tabulate

from src.data_collection import DataCollector
from src.mood_tracking import MoodTracker
from src.pattern_recognition import PatternRecognitionEngine
from src.correlation_analysis import CorrelationAnalyzer
from src.visualization import VisualizationGenerator

class UserInterface:
    """
    Command-line interface for the Mental Health Pattern Recognition Assistant.
    """
    
    def __init__(self, data_dir: str = "../data", output_dir: str = "../visualization"):
        """
        Initialize the user interface with data and output directories.
        
        Args:
            data_dir: Directory for data storage
            output_dir: Directory for visualization output
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        
        # Ensure directories exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.data_collector = DataCollector(data_dir=data_dir)
        self.mood_tracker = MoodTracker(data_collector=self.data_collector)
        self.pattern_engine = PatternRecognitionEngine(data_collector=self.data_collector)
        self.correlation_analyzer = CorrelationAnalyzer(data_collector=self.data_collector)
        self.visualization_generator = VisualizationGenerator(
            data_collector=self.data_collector,
            output_dir=output_dir
        )
        
        # Set up color codes for terminal output
        self.colors = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "green": "\033[92m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "yellow": "\033[93m",
            "red": "\033[91m",
            "magenta": "\033[95m",
            "header": "\033[1;95m",  # Bold magenta
            "title": "\033[1;96m",   # Bold cyan
            "success": "\033[1;92m", # Bold green
            "warning": "\033[1;93m", # Bold yellow
            "error": "\033[1;91m",   # Bold red
            "prompt": "\033[1;94m"   # Bold blue
        }
    
    def run(self):
        """
        Run the main application loop.
        """
        self._print_welcome()
        
        while True:
            self._print_main_menu()
            choice = input(f"{self.colors['prompt']}Enter your choice (1-7): {self.colors['reset']}")
            
            if choice == '1':
                self._data_entry_menu()
            elif choice == '2':
                self._view_data_menu()
            elif choice == '3':
                self._analysis_menu()
            elif choice == '4':
                self._visualization_menu()
            elif choice == '5':
                self._insights_menu()
            elif choice == '6':
                self._settings_menu()
            elif choice == '7':
                print(f"\n{self.colors['success']}Thank you for using the Mental Health Pattern Recognition Assistant. Goodbye!{self.colors['reset']}\n")
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _print_welcome(self):
        """Print welcome message."""
        print("\n" + "=" * 80)
        print(f"{self.colors['header']}Welcome to the Mental Health Pattern Recognition Assistant{self.colors['reset']}")
        print("=" * 80)
        print(f"\nThis application helps you track your mood and identify patterns and correlations")
        print(f"that can provide insights into factors affecting your mental wellbeing.")
        print("\n" + "-" * 80 + "\n")
    
    def _print_main_menu(self):
        """Print the main menu options."""
        print(f"\n{self.colors['title']}Main Menu:{self.colors['reset']}")
        print(f"  1. {self.colors['cyan']}Data Entry{self.colors['reset']} - Record mood, activities, sleep, and more")
        print(f"  2. {self.colors['cyan']}View Data{self.colors['reset']} - Browse your recorded data")
        print(f"  3. {self.colors['cyan']}Analysis{self.colors['reset']} - Run pattern recognition and correlation analysis")
        print(f"  4. {self.colors['cyan']}Visualizations{self.colors['reset']} - Generate charts and graphs")
        print(f"  5. {self.colors['cyan']}Insights{self.colors['reset']} - View personalized insights and recommendations")
        print(f"  6. {self.colors['cyan']}Settings{self.colors['reset']} - Configure application settings")
        print(f"  7. {self.colors['cyan']}Exit{self.colors['reset']} - Close the application")
        print()
    
    def _data_entry_menu(self):
        """Display and handle the data entry menu."""
        while True:
            print(f"\n{self.colors['title']}Data Entry Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}Record Mood{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}Record Activity{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}Record Sleep{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}Record Medication{self.colors['reset']}")
            print(f"  5. {self.colors['cyan']}Record Custom Entry{self.colors['reset']}")
            print(f"  6. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-6): {self.colors['reset']}")
            
            if choice == '1':
                self._record_mood()
            elif choice == '2':
                self._record_activity()
            elif choice == '3':
                self._record_sleep()
            elif choice == '4':
                self._record_medication()
            elif choice == '5':
                self._record_custom_entry()
            elif choice == '6':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _record_mood(self):
        """Record a mood entry."""
        print(f"\n{self.colors['title']}Record Mood:{self.colors['reset']}")
        
        # Get mood level
        while True:
            try:
                mood_level = int(input(f"Enter your mood level (1-10, where 10 is best): "))
                if 1 <= mood_level <= 10:
                    break
                else:
                    print(f"{self.colors['error']}Please enter a number between 1 and 10.{self.colors['reset']}")
            except ValueError:
                print(f"{self.colors['error']}Please enter a valid number.{self.colors['reset']}")
        
        # Get notes
        notes = input("Enter any notes about your mood (optional): ")
        
        # Get emotions
        emotions_input = input("Enter emotions you're experiencing (comma-separated, e.g., happy,calm): ")
        emotions = [e.strip() for e in emotions_input.split(',')] if emotions_input.strip() else []
        
        # Record mood
        entry = self.mood_tracker.log_mood(
            mood_level=mood_level,
            notes=notes,
            emotions=emotions
        )
        
        print(f"\n{self.colors['success']}Mood recorded successfully!{self.colors['reset']}")
        
        # Show quick summary
        print(f"\nQuick Summary:")
        print(f"  Mood Level: {mood_level}/10")
        if emotions:
            print(f"  Emotions: {', '.join(emotions)}")
        if notes:
            print(f"  Notes: {notes}")
        
        # Offer to show recent mood history
        show_history = input("\nWould you like to see your recent mood history? (y/n): ").lower()
        if show_history == 'y':
            self._show_recent_mood_history()
    
    def _record_activity(self):
        """Record an activity entry."""
        print(f"\n{self.colors['title']}Record Activity:{self.colors['reset']}")
        
        # Get activity type
        activity_type = input("Enter activity type (e.g., exercise, work, social): ")
        
        # Get duration
        while True:
            try:
                duration = input("Enter duration in minutes: ")
                if duration:
                    duration_minutes = int(duration)
                    if duration_minutes > 0:
                        break
                    else:
                        print(f"{self.colors['error']}Duration must be greater than 0.{self.colors['reset']}")
                else:
                    duration_minutes = None
                    break
            except ValueError:
                print(f"{self.colors['error']}Please enter a valid number.{self.colors['reset']}")
        
        # Get intensity
        intensity = None
        intensity_input = input("Enter intensity level (1-5, where 5 is most intense, optional): ")
        if intensity_input:
            try:
                intensity = int(intensity_input)
                if not 1 <= intensity <= 5:
                    print(f"{self.colors['warning']}Intensity should be between 1-5. Using default value.{self.colors['reset']}")
                    intensity = None
            except ValueError:
                print(f"{self.colors['warning']}Invalid intensity. Using default value.{self.colors['reset']}")
        
        # Get notes
        notes = input("Enter any notes about this activity (optional): ")
        
        # Record activity
        entry = self.data_collector.record_activity(
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            intensity=intensity,
            notes=notes
        )
        
        print(f"\n{self.colors['success']}Activity recorded successfully!{self.colors['reset']}")
        
        # Show quick summary
        print(f"\nQuick Summary:")
        print(f"  Activity: {activity_type}")
        if duration_minutes:
            print(f"  Duration: {duration_minutes} minutes")
        if intensity:
            print(f"  Intensity: {intensity}/5")
        if notes:
            print(f"  Notes: {notes}")
    
    def _record_sleep(self):
        """Record a sleep entry."""
        print(f"\n{self.colors['title']}Record Sleep:{self.colors['reset']}")
        
        # Get sleep duration
        while True:
            try:
                duration_input = input("Enter sleep duration in hours (e.g., 7.5): ")
                duration_hours = float(duration_input)
                if 0 < duration_hours <= 24:
                    break
                else:
                    print(f"{self.colors['error']}Duration must be between 0 and 24 hours.{self.colors['reset']}")
            except ValueError:
                print(f"{self.colors['error']}Please enter a valid number.{self.colors['reset']}")
        
        # Get sleep quality
        quality = None
        quality_input = input("Enter sleep quality (1-10, where 10 is best, optional): ")
        if quality_input:
            try:
                quality = int(quality_input)
                if not 1 <= quality <= 10:
                    print(f"{self.colors['warning']}Quality should be between 1-10. Using default value.{self.colors['reset']}")
                    quality = None
            except ValueError:
                print(f"{self.colors['warning']}Invalid quality. Using default value.{self.colors['reset']}")
        
        # Get sleep times
        start_time_input = input("Enter sleep start time (e.g., 23:00, optional): ")
        start_time = None
        if start_time_input:
            try:
                # Parse time and combine with today's date
                hour, minute = map(int, start_time_input.split(':'))
                now = datetime.datetime.now()
                start_time = now.replace(hour=hour, minute=minute).isoformat()
            except (ValueError, TypeError):
                print(f"{self.colors['warning']}Invalid time format. Using current time.{self.colors['reset']}")
        
        end_time_input = input("Enter sleep end time (e.g., 07:30, optional): ")
        end_time = None
        if end_time_input:
            try:
                # Parse time and combine with today's date
                hour, minute = map(int, end_time_input.split(':'))
                now = datetime.datetime.now()
                end_time = now.replace(hour=hour, minute=minute).isoformat()
            except (ValueError, TypeError):
                print(f"{self.colors['warning']}Invalid time format. Using current time.{self.colors['reset']}")
        
        # Get notes
        notes = input("Enter any notes about your sleep (optional): ")
        
        # Record sleep
        entry = self.data_collector.record_sleep(
            duration_hours=duration_hours,
            quality=quality,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )
        
        print(f"\n{self.colors['success']}Sleep recorded successfully!{self.colors['reset']}")
        
        # Show quick summary
        print(f"\nQuick Summary:")
        print(f"  Duration: {duration_hours} hours")
        if quality:
            print(f"  Quality: {quality}/10")
        if start_time:
            print(f"  Start Time: {start_time_input}")
        if end_time:
            print(f"  End Time: {end_time_input}")
        if notes:
            print(f"  Notes: {notes}")
    
    def _record_medication(self):
        """Record a medication entry."""
        print(f"\n{self.colors['title']}Record Medication:{self.colors['reset']}")
        
        # Get medication name
        medication_name = input("Enter medication name: ")
        
        # Get dosage
        dosage = input("Enter dosage (e.g., 10mg, optional): ")
        
        # Get taken status
        taken_input = input("Did you take this medication? (y/n, default: y): ").lower()
        taken = taken_input != 'n'
        
        # Get notes
        notes = input("Enter any notes about this medication (optional): ")
        
        # Record medication
        entry = self.data_collector.record_medication(
            medication_name=medication_name,
            dosage=dosage,
            taken=taken,
            notes=notes
        )
        
        print(f"\n{self.colors['success']}Medication recorded successfully!{self.colors['reset']}")
        
        # Show quick summary
        print(f"\nQuick Summary:")
        print(f"  Medication: {medication_name}")
        if dosage:
            print(f"  Dosage: {dosage}")
        print(f"  Taken: {'Yes' if taken else 'No'}")
        if notes:
            print(f"  Notes: {notes}")
    
    def _record_custom_entry(self):
        """Record a custom entry."""
        print(f"\n{self.colors['title']}Record Custom Entry:{self.colors['reset']}")
        
        # Get category
        category = input("Enter custom category name: ")
        
        # Get values
        print("\nEnter key-value pairs (one per line, leave blank to finish):")
        print("Example: energy_level: 8")
        
        values = {}
        while True:
            line = input("> ")
            if not line:
                break
                
            try:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Try to convert value to number if possible
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    # Keep as string if not a number
                    pass
                    
                values[key] = value
            except ValueError:
                print(f"{self.colors['error']}Invalid format. Use 'key: value' format.{self.colors['reset']}")
        
        if not values:
            print(f"{self.colors['error']}No values entered. Cancelling custom entry.{self.colors['reset']}")
            return
        
        # Record custom entry
        entry = self.data_collector.record_custom_entry(
            category=category,
            values=values
        )
        
        print(f"\n{self.colors['success']}Custom entry recorded successfully!{self.colors['reset']}")
        
        # Show quick summary
        print(f"\nQuick Summary:")
        print(f"  Category: {category}")
        print("  Values:")
        for key, value in values.items():
            print(f"    {key}: {value}")
    
    def _view_data_menu(self):
        """Display and handle the view data menu."""
        while True:
            print(f"\n{self.colors['title']}View Data Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}View Mood Entries{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}View Activity Entries{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}View Sleep Entries{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}View Medication Entries{self.colors['reset']}")
            print(f"  5. {self.colors['cyan']}View Custom Entries{self.colors['reset']}")
            print(f"  6. {self.colors['cyan']}View All Data{self.colors['reset']}")
            print(f"  7. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-7): {self.colors['reset']}")
            
            if choice == '1':
                self._view_mood_entries()
            elif choice == '2':
                self._view_activity_entries()
            elif choice == '3':
                self._view_sleep_entries()
            elif choice == '4':
                self._view_medication_entries()
            elif choice == '5':
                self._view_custom_entries()
            elif choice == '6':
                self._view_all_data()
            elif choice == '7':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _view_mood_entries(self):
        """View mood entries."""
        print(f"\n{self.colors['title']}Mood Entries:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get mood entries
        mood_entries = self._get_entries_for_period("mood_entries", days)
        
        if not mood_entries:
            print(f"{self.colors['warning']}No mood entries found for the selected period.{self.colors['reset']}")
            return
        
        # Prepare data for display
        table_data = []
        for entry in mood_entries:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M")
            
            emotions = ", ".join(entry.get("emotions", [])) if entry.get("emotions") else ""
            notes = entry.get("notes", "")
            
            table_data.append([
                formatted_date,
                entry["mood_level"],
                emotions,
                notes
            ])
        
        # Display table
        headers = ["Date & Time", "Mood Level", "Emotions", "Notes"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Show summary statistics
        mood_levels = [entry["mood_level"] for entry in mood_entries]
        avg_mood = sum(mood_levels) / len(mood_levels)
        min_mood = min(mood_levels)
        max_mood = max(mood_levels)
        
        print(f"\nSummary Statistics:")
        print(f"  Total Entries: {len(mood_entries)}")
        print(f"  Average Mood: {avg_mood:.1f}")
        print(f"  Mood Range: {min_mood} - {max_mood}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a mood timeline visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_mood_timeline(days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _view_activity_entries(self):
        """View activity entries."""
        print(f"\n{self.colors['title']}Activity Entries:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get activity entries
        activity_entries = self._get_entries_for_period("activity_entries", days)
        
        if not activity_entries:
            print(f"{self.colors['warning']}No activity entries found for the selected period.{self.colors['reset']}")
            return
        
        # Prepare data for display
        table_data = []
        for entry in activity_entries:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M")
            
            duration = entry.get("duration_minutes", "")
            intensity = entry.get("intensity", "")
            notes = entry.get("notes", "")
            
            table_data.append([
                formatted_date,
                entry["activity_type"],
                duration,
                intensity,
                notes
            ])
        
        # Display table
        headers = ["Date & Time", "Activity", "Duration (min)", "Intensity", "Notes"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Show summary statistics
        activity_types = {}
        for entry in activity_entries:
            activity_type = entry["activity_type"]
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
        
        print(f"\nSummary Statistics:")
        print(f"  Total Entries: {len(activity_entries)}")
        print(f"  Activity Types:")
        for activity, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
            print(f"    {activity}: {count} entries")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a mood-activity correlation visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_mood_activity_correlation(days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _view_sleep_entries(self):
        """View sleep entries."""
        print(f"\n{self.colors['title']}Sleep Entries:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get sleep entries
        sleep_entries = self._get_entries_for_period("sleep_entries", days)
        
        if not sleep_entries:
            print(f"{self.colors['warning']}No sleep entries found for the selected period.{self.colors['reset']}")
            return
        
        # Prepare data for display
        table_data = []
        for entry in sleep_entries:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            formatted_date = timestamp.strftime("%Y-%m-%d")
            
            duration = entry.get("duration_hours", "")
            quality = entry.get("quality", "")
            notes = entry.get("notes", "")
            
            table_data.append([
                formatted_date,
                duration,
                quality,
                notes
            ])
        
        # Display table
        headers = ["Date", "Duration (hours)", "Quality", "Notes"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Show summary statistics
        durations = [entry["duration_hours"] for entry in sleep_entries if "duration_hours" in entry]
        qualities = [entry["quality"] for entry in sleep_entries if "quality" in entry]
        
        if durations:
            avg_duration = sum(durations) / len(durations)
            print(f"\nSummary Statistics:")
            print(f"  Total Entries: {len(sleep_entries)}")
            print(f"  Average Sleep Duration: {avg_duration:.1f} hours")
            
            if qualities:
                avg_quality = sum(qualities) / len(qualities)
                print(f"  Average Sleep Quality: {avg_quality:.1f}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a mood-sleep correlation visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_mood_sleep_correlation(days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _view_medication_entries(self):
        """View medication entries."""
        print(f"\n{self.colors['title']}Medication Entries:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get medication entries
        medication_entries = self._get_entries_for_period("medication_entries", days)
        
        if not medication_entries:
            print(f"{self.colors['warning']}No medication entries found for the selected period.{self.colors['reset']}")
            return
        
        # Prepare data for display
        table_data = []
        for entry in medication_entries:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M")
            
            dosage = entry.get("dosage", "")
            taken = "Yes" if entry.get("taken", True) else "No"
            notes = entry.get("notes", "")
            
            table_data.append([
                formatted_date,
                entry["medication_name"],
                dosage,
                taken,
                notes
            ])
        
        # Display table
        headers = ["Date & Time", "Medication", "Dosage", "Taken", "Notes"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Show summary statistics
        medication_types = {}
        for entry in medication_entries:
            medication_name = entry["medication_name"]
            medication_types[medication_name] = medication_types.get(medication_name, 0) + 1
        
        print(f"\nSummary Statistics:")
        print(f"  Total Entries: {len(medication_entries)}")
        print(f"  Medication Types:")
        for medication, count in sorted(medication_types.items(), key=lambda x: x[1], reverse=True):
            print(f"    {medication}: {count} entries")
    
    def _view_custom_entries(self):
        """View custom entries."""
        print(f"\n{self.colors['title']}Custom Entries:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get custom entries
        custom_entries = self._get_entries_for_period("custom_entries", days)
        
        if not custom_entries:
            print(f"{self.colors['warning']}No custom entries found for the selected period.{self.colors['reset']}")
            return
        
        # Group by category
        categories = {}
        for entry in custom_entries:
            category = entry["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(entry)
        
        # Display entries by category
        for category, entries in categories.items():
            print(f"\n{self.colors['title']}{category} Entries:{self.colors['reset']}")
            
            # Prepare data for display
            table_data = []
            for entry in entries:
                timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
                formatted_date = timestamp.strftime("%Y-%m-%d %H:%M")
                
                values_str = ", ".join([f"{k}: {v}" for k, v in entry["values"].items()])
                
                table_data.append([
                    formatted_date,
                    values_str
                ])
            
            # Display table
            headers = ["Date & Time", "Values"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            print(f"  Total {category} Entries: {len(entries)}")
    
    def _view_all_data(self):
        """View summary of all data."""
        print(f"\n{self.colors['title']}All Data Summary:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get all data
        all_data = self.data_collector.get_all_data()
        
        # Calculate entry counts
        mood_count = len(all_data.get("mood_entries", []))
        activity_count = len(all_data.get("activity_entries", []))
        sleep_count = len(all_data.get("sleep_entries", []))
        medication_count = len(all_data.get("medication_entries", []))
        custom_count = len(all_data.get("custom_entries", []))
        
        total_count = mood_count + activity_count + sleep_count + medication_count + custom_count
        
        # Display summary
        print(f"\nData Summary:")
        print(f"  Total Entries: {total_count}")
        print(f"  Mood Entries: {mood_count}")
        print(f"  Activity Entries: {activity_count}")
        print(f"  Sleep Entries: {sleep_count}")
        print(f"  Medication Entries: {medication_count}")
        print(f"  Custom Entries: {custom_count}")
        
        # Offer to show dashboard
        show_dashboard = input("\nWould you like to see a comprehensive dashboard visualization? (y/n): ").lower()
        if show_dashboard == 'y':
            print(f"\n{self.colors['cyan']}Generating dashboard... This may take a moment.{self.colors['reset']}")
            dashboard_path = self.visualization_generator.generate_dashboard(days=days)
            print(f"\n{self.colors['success']}Dashboard saved to: {dashboard_path}{self.colors['reset']}")
            print(f"Opening dashboard...")
            self._show_image(dashboard_path)
    
    def _analysis_menu(self):
        """Display and handle the analysis menu."""
        while True:
            print(f"\n{self.colors['title']}Analysis Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}Run Pattern Recognition{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}Run Correlation Analysis{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}Generate Mood Summary{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}Generate Comprehensive Analysis{self.colors['reset']}")
            print(f"  5. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-5): {self.colors['reset']}")
            
            if choice == '1':
                self._run_pattern_recognition()
            elif choice == '2':
                self._run_correlation_analysis()
            elif choice == '3':
                self._generate_mood_summary()
            elif choice == '4':
                self._generate_comprehensive_analysis()
            elif choice == '5':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _run_pattern_recognition(self):
        """Run pattern recognition analysis."""
        print(f"\n{self.colors['title']}Pattern Recognition Analysis:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Running pattern recognition analysis... This may take a moment.{self.colors['reset']}")
        
        # Run pattern recognition
        patterns = self.pattern_engine.identify_mood_patterns(days=days)
        
        if patterns.get("status") != "success":
            print(f"\n{self.colors['error']}Insufficient data for pattern recognition. Please record more data.{self.colors['reset']}")
            return
        
        # Display time of day patterns
        time_of_day = patterns.get("time_of_day", {})
        print(f"\n{self.colors['title']}Time of Day Patterns:{self.colors['reset']}")
        print(f"  Morning Mood: {time_of_day.get('morning', 'N/A')}")
        print(f"  Afternoon Mood: {time_of_day.get('afternoon', 'N/A')}")
        print(f"  Evening Mood: {time_of_day.get('evening', 'N/A')}")
        
        best_time = time_of_day.get("best_time")
        if best_time:
            print(f"  Best Time of Day: {best_time.title()}")
        
        # Display day of week patterns
        day_of_week = patterns.get("day_of_week", {})
        print(f"\n{self.colors['title']}Day of Week Patterns:{self.colors['reset']}")
        print(f"  Weekday Mood: {day_of_week.get('weekday', 'N/A')}")
        print(f"  Weekend Mood: {day_of_week.get('weekend', 'N/A')}")
        
        better_period = day_of_week.get("better_period")
        if better_period and better_period != "similar":
            print(f"  Better Period: {better_period.title()}")
        
        # Display trend analysis
        trend_analysis = patterns.get("trend_analysis", {})
        if trend_analysis:
            print(f"\n{self.colors['title']}Trend Analysis:{self.colors['reset']}")
            
            direction = trend_analysis.get("direction")
            if direction:
                print(f"  Overall Trend: {direction.title()}")
            
            weekly_direction = trend_analysis.get("weekly_direction")
            if weekly_direction:
                print(f"  Weekly Trend: {weekly_direction.title()}")
        
        # Display insights
        insights = patterns.get("insights", [])
        if insights:
            print(f"\n{self.colors['title']}Pattern Insights:{self.colors['reset']}")
            for i, insight in enumerate(insights):
                print(f"  {i+1}. {insight}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a pattern visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_pattern_visualization(patterns, days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _run_correlation_analysis(self):
        """Run correlation analysis."""
        print(f"\n{self.colors['title']}Correlation Analysis:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Running correlation analysis... This may take a moment.{self.colors['reset']}")
        
        # Run correlation analysis
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis(days=days)
        
        # Check if we have valid results
        if all(corr.get("status") != "success" for corr in correlations.values() if isinstance(corr, dict)):
            print(f"\n{self.colors['error']}Insufficient data for correlation analysis. Please record more data.{self.colors['reset']}")
            return
        
        # Display lagged correlations
        lagged_correlations = correlations.get("lagged_correlations", {})
        if lagged_correlations.get("status") == "success":
            print(f"\n{self.colors['title']}Lagged Correlations:{self.colors['reset']}")
            
            lag_results = lagged_correlations.get("lag_results", [])
            if lag_results:
                for i, result in enumerate(lag_results[:3]):  # Show top 3
                    var_name = result["variable"].replace("_", " ").title()
                    strongest = result["strongest_lag"]
                    
                    print(f"  {i+1}. {var_name} (Lag {strongest['lag']} days): {strongest['correlation']:.2f}")
                    print(f"     {'Significant' if strongest['significant'] else 'Not significant'}")
        
        # Display Granger causality
        granger_causality = correlations.get("granger_causality", {})
        if granger_causality.get("status") == "success":
            print(f"\n{self.colors['title']}Granger Causality:{self.colors['reset']}")
            
            causality_results = granger_causality.get("causality_results", [])
            if causality_results:
                for i, result in enumerate(causality_results[:3]):  # Show top 3
                    var_name = result["variable"].replace("_", " ").title()
                    direction = result["direction"]
                    lag = result["most_significant_lag"]["lag"]
                    
                    print(f"  {i+1}. {direction} (Lag {lag} days)")
                    print(f"     p-value: {result['most_significant_lag']['p_value']:.4f}")
        
        # Display mood cycles
        mood_cycles = correlations.get("mood_cycles", {})
        if mood_cycles.get("status") == "success":
            print(f"\n{self.colors['title']}Mood Cycles:{self.colors['reset']}")
            
            cycles = mood_cycles.get("cycles", [])
            if cycles:
                for i, cycle in enumerate(cycles):
                    print(f"  {i+1}. {cycle['length']}-day cycle (Strength: {cycle['strength']:.2f}, Type: {cycle['type']})")
        
        # Display key insights
        key_insights = correlations.get("key_insights", [])
        if key_insights:
            print(f"\n{self.colors['title']}Key Correlation Insights:{self.colors['reset']}")
            for i, insight in enumerate(key_insights):
                print(f"  {i+1}. {insight}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a correlation visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_correlation_visualization(correlations, days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _generate_mood_summary(self):
        """Generate a mood summary."""
        print(f"\n{self.colors['title']}Mood Summary:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating mood summary... This may take a moment.{self.colors['reset']}")
        
        # Generate mood summary
        summary = self.mood_tracker.generate_mood_summary(days=days)
        
        if summary.get("status") != "success":
            print(f"\n{self.colors['error']}Insufficient mood data for summary. Please record more mood entries.{self.colors['reset']}")
            return
        
        # Display summary statistics
        stats = summary.get("statistics", {})
        print(f"\n{self.colors['title']}Mood Statistics:{self.colors['reset']}")
        print(f"  Average Mood: {stats.get('average_mood', 'N/A'):.1f}")
        
        mood_range = stats.get("mood_range", [0, 0])
        print(f"  Mood Range: {mood_range[0]} - {mood_range[1]}")
        
        print(f"  Mood Volatility: {stats.get('mood_volatility', 'N/A'):.2f}")
        
        # Display emotion data
        emotions = summary.get("emotions", {})
        common_emotions = emotions.get("common_emotions", [])
        
        if common_emotions:
            print(f"\n{self.colors['title']}Common Emotions:{self.colors['reset']}")
            for i, (emotion, count) in enumerate(common_emotions):
                print(f"  {i+1}. {emotion}: {count} occurrences")
        
        # Display emotion distribution
        distribution = emotions.get("category_distribution", {})
        if distribution:
            print(f"\n{self.colors['title']}Emotion Category Distribution:{self.colors['reset']}")
            print(f"  Positive: {distribution.get('positive', 0):.1f}%")
            print(f"  Negative: {distribution.get('negative', 0):.1f}%")
            print(f"  Neutral: {distribution.get('neutral', 0):.1f}%")
        
        # Display insights
        insights = summary.get("insights", [])
        if insights:
            print(f"\n{self.colors['title']}Mood Insights:{self.colors['reset']}")
            for i, insight in enumerate(insights):
                print(f"  {i+1}. {insight}")
        
        # Show visualizations
        visualizations = summary.get("visualizations", {})
        
        timeline_plot = visualizations.get("timeline_plot")
        if timeline_plot:
            show_timeline = input("\nWould you like to see the mood timeline plot? (y/n): ").lower()
            if show_timeline == 'y':
                print(f"Opening mood timeline visualization...")
                self._show_image(timeline_plot)
        
        emotion_plot = visualizations.get("emotion_plot")
        if emotion_plot:
            show_emotion = input("\nWould you like to see the emotion distribution plot? (y/n): ").lower()
            if show_emotion == 'y':
                print(f"Opening emotion distribution visualization...")
                self._show_image(emotion_plot)
    
    def _generate_comprehensive_analysis(self):
        """Generate a comprehensive analysis."""
        print(f"\n{self.colors['title']}Comprehensive Analysis:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating comprehensive analysis... This may take a moment.{self.colors['reset']}")
        
        # Run pattern recognition
        patterns = self.pattern_engine.identify_mood_patterns(days=days)
        
        # Run correlation analysis
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis(days=days)
        
        # Check if we have valid results
        if patterns.get("status") != "success" and all(corr.get("status") != "success" for corr in correlations.values() if isinstance(corr, dict)):
            print(f"\n{self.colors['error']}Insufficient data for comprehensive analysis. Please record more data.{self.colors['reset']}")
            return
        
        # Compile all insights
        all_insights = []
        
        # Add pattern insights
        if patterns.get("status") == "success":
            pattern_insights = patterns.get("insights", [])
            if pattern_insights:
                all_insights.extend(pattern_insights)
        
        # Add correlation insights
        key_insights = correlations.get("key_insights", [])
        if key_insights:
            all_insights.extend(key_insights)
        
        # Display all insights
        if all_insights:
            print(f"\n{self.colors['title']}Key Insights:{self.colors['reset']}")
            for i, insight in enumerate(all_insights):
                print(f"  {i+1}. {insight}")
        else:
            print(f"\n{self.colors['warning']}No significant insights found. Try recording more varied data.{self.colors['reset']}")
        
        # Offer to show dashboard
        show_dashboard = input("\nWould you like to see a comprehensive dashboard visualization? (y/n): ").lower()
        if show_dashboard == 'y':
            print(f"\n{self.colors['cyan']}Generating dashboard... This may take a moment.{self.colors['reset']}")
            dashboard_path = self.visualization_generator.generate_dashboard(days=days)
            print(f"\n{self.colors['success']}Dashboard saved to: {dashboard_path}{self.colors['reset']}")
            print(f"Opening dashboard...")
            self._show_image(dashboard_path)
    
    def _visualization_menu(self):
        """Display and handle the visualization menu."""
        while True:
            print(f"\n{self.colors['title']}Visualization Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}Generate Mood Timeline{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}Generate Mood by Day of Week{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}Generate Emotion Distribution{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}Generate Activity-Mood Correlation{self.colors['reset']}")
            print(f"  5. {self.colors['cyan']}Generate Sleep-Mood Correlation{self.colors['reset']}")
            print(f"  6. {self.colors['cyan']}Generate Pattern Visualization{self.colors['reset']}")
            print(f"  7. {self.colors['cyan']}Generate Correlation Visualization{self.colors['reset']}")
            print(f"  8. {self.colors['cyan']}Generate Dashboard{self.colors['reset']}")
            print(f"  9. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-9): {self.colors['reset']}")
            
            if choice == '1':
                self._generate_mood_timeline()
            elif choice == '2':
                self._generate_mood_by_day()
            elif choice == '3':
                self._generate_emotion_distribution()
            elif choice == '4':
                self._generate_activity_mood_correlation()
            elif choice == '5':
                self._generate_sleep_mood_correlation()
            elif choice == '6':
                self._generate_pattern_visualization()
            elif choice == '7':
                self._generate_correlation_visualization()
            elif choice == '8':
                self._generate_dashboard()
            elif choice == '9':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _generate_mood_timeline(self):
        """Generate a mood timeline visualization."""
        print(f"\n{self.colors['title']}Generate Mood Timeline:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating mood timeline... This may take a moment.{self.colors['reset']}")
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_timeline(days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_mood_by_day(self):
        """Generate a mood by day of week visualization."""
        print(f"\n{self.colors['title']}Generate Mood by Day of Week:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating mood by day of week... This may take a moment.{self.colors['reset']}")
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_by_day_of_week(days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_emotion_distribution(self):
        """Generate an emotion distribution visualization."""
        print(f"\n{self.colors['title']}Generate Emotion Distribution:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating emotion distribution... This may take a moment.{self.colors['reset']}")
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_emotion_distribution(days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_activity_mood_correlation(self):
        """Generate an activity-mood correlation visualization."""
        print(f"\n{self.colors['title']}Generate Activity-Mood Correlation:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        # Get activity entries to check available types
        activity_entries = self._get_entries_for_period("activity_entries", days)
        
        if not activity_entries:
            print(f"\n{self.colors['error']}No activity entries found for the selected period.{self.colors['reset']}")
            return
        
        # Get unique activity types
        activity_types = set()
        for entry in activity_entries:
            activity_types.add(entry["activity_type"])
        
        # Ask if user wants to filter by specific activity
        print(f"\nAvailable activity types: {', '.join(sorted(activity_types))}")
        filter_by_activity = input("Would you like to filter by a specific activity type? (y/n): ").lower()
        
        activity_type = None
        if filter_by_activity == 'y':
            activity_type = input("Enter activity type: ")
            if activity_type not in activity_types:
                print(f"{self.colors['warning']}Activity type not found. Showing all activities.{self.colors['reset']}")
                activity_type = None
        
        print(f"\n{self.colors['cyan']}Generating activity-mood correlation... This may take a moment.{self.colors['reset']}")
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_activity_correlation(
            activity_type=activity_type,
            days=days
        )
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_sleep_mood_correlation(self):
        """Generate a sleep-mood correlation visualization."""
        print(f"\n{self.colors['title']}Generate Sleep-Mood Correlation:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating sleep-mood correlation... This may take a moment.{self.colors['reset']}")
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_mood_sleep_correlation(days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_pattern_visualization(self):
        """Generate a pattern visualization."""
        print(f"\n{self.colors['title']}Generate Pattern Visualization:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Running pattern recognition and generating visualization... This may take a moment.{self.colors['reset']}")
        
        # Run pattern recognition
        patterns = self.pattern_engine.identify_mood_patterns(days=days)
        
        if patterns.get("status") != "success":
            print(f"\n{self.colors['error']}Insufficient data for pattern recognition. Please record more data.{self.colors['reset']}")
            return
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_pattern_visualization(patterns, days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_correlation_visualization(self):
        """Generate a correlation visualization."""
        print(f"\n{self.colors['title']}Generate Correlation Visualization:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Running correlation analysis and generating visualization... This may take a moment.{self.colors['reset']}")
        
        # Run correlation analysis
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis(days=days)
        
        # Check if we have valid results
        if all(corr.get("status") != "success" for corr in correlations.values() if isinstance(corr, dict)):
            print(f"\n{self.colors['error']}Insufficient data for correlation analysis. Please record more data.{self.colors['reset']}")
            return
        
        # Generate visualization
        viz_path = self.visualization_generator.generate_correlation_visualization(correlations, days=days)
        
        print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
        print(f"Opening visualization...")
        self._show_image(viz_path)
    
    def _generate_dashboard(self):
        """Generate a comprehensive dashboard."""
        print(f"\n{self.colors['title']}Generate Dashboard:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating dashboard... This may take a moment.{self.colors['reset']}")
        
        # Generate dashboard
        dashboard_path = self.visualization_generator.generate_dashboard(days=days)
        
        print(f"\n{self.colors['success']}Dashboard saved to: {dashboard_path}{self.colors['reset']}")
        print(f"Opening dashboard...")
        self._show_image(dashboard_path)
    
    def _insights_menu(self):
        """Display and handle the insights menu."""
        while True:
            print(f"\n{self.colors['title']}Insights Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}View Pattern Insights{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}View Correlation Insights{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}View Comprehensive Insights{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-4): {self.colors['reset']}")
            
            if choice == '1':
                self._view_pattern_insights()
            elif choice == '2':
                self._view_correlation_insights()
            elif choice == '3':
                self._view_comprehensive_insights()
            elif choice == '4':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _view_pattern_insights(self):
        """View pattern insights."""
        print(f"\n{self.colors['title']}Pattern Insights:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Analyzing patterns... This may take a moment.{self.colors['reset']}")
        
        # Run pattern recognition
        patterns = self.pattern_engine.identify_mood_patterns(days=days)
        
        if patterns.get("status") != "success":
            print(f"\n{self.colors['error']}Insufficient data for pattern recognition. Please record more data.{self.colors['reset']}")
            return
        
        # Display insights
        insights = patterns.get("insights", [])
        if insights:
            print(f"\n{self.colors['title']}Key Pattern Insights:{self.colors['reset']}")
            for i, insight in enumerate(insights):
                print(f"  {i+1}. {insight}")
        else:
            print(f"\n{self.colors['warning']}No significant pattern insights found. Try recording more varied data.{self.colors['reset']}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a pattern visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_pattern_visualization(patterns, days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _view_correlation_insights(self):
        """View correlation insights."""
        print(f"\n{self.colors['title']}Correlation Insights:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Analyzing correlations... This may take a moment.{self.colors['reset']}")
        
        # Run correlation analysis
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis(days=days)
        
        # Check if we have valid results
        if all(corr.get("status") != "success" for corr in correlations.values() if isinstance(corr, dict)):
            print(f"\n{self.colors['error']}Insufficient data for correlation analysis. Please record more data.{self.colors['reset']}")
            return
        
        # Display key insights
        key_insights = correlations.get("key_insights", [])
        if key_insights:
            print(f"\n{self.colors['title']}Key Correlation Insights:{self.colors['reset']}")
            for i, insight in enumerate(key_insights):
                print(f"  {i+1}. {insight}")
        else:
            print(f"\n{self.colors['warning']}No significant correlation insights found. Try recording more varied data.{self.colors['reset']}")
        
        # Display all insights
        all_insights = correlations.get("all_insights", [])
        if all_insights and len(all_insights) > len(key_insights):
            show_all = input("\nWould you like to see all correlation insights? (y/n): ").lower()
            if show_all == 'y':
                print(f"\n{self.colors['title']}All Correlation Insights:{self.colors['reset']}")
                for i, insight in enumerate(all_insights):
                    print(f"  {i+1}. {insight}")
        
        # Offer to show visualization
        show_viz = input("\nWould you like to see a correlation visualization? (y/n): ").lower()
        if show_viz == 'y':
            viz_path = self.visualization_generator.generate_correlation_visualization(correlations, days=days)
            print(f"\n{self.colors['success']}Visualization saved to: {viz_path}{self.colors['reset']}")
            print(f"Opening visualization...")
            self._show_image(viz_path)
    
    def _view_comprehensive_insights(self):
        """View comprehensive insights."""
        print(f"\n{self.colors['title']}Comprehensive Insights:{self.colors['reset']}")
        
        # Get time period
        days = self._get_time_period()
        
        print(f"\n{self.colors['cyan']}Generating comprehensive insights... This may take a moment.{self.colors['reset']}")
        
        # Run pattern recognition
        patterns = self.pattern_engine.identify_mood_patterns(days=days)
        
        # Run correlation analysis
        correlations = self.correlation_analyzer.generate_comprehensive_correlation_analysis(days=days)
        
        # Check if we have valid results
        if patterns.get("status") != "success" and all(corr.get("status") != "success" for corr in correlations.values() if isinstance(corr, dict)):
            print(f"\n{self.colors['error']}Insufficient data for comprehensive insights. Please record more data.{self.colors['reset']}")
            return
        
        # Compile all insights
        all_insights = []
        
        # Add pattern insights
        if patterns.get("status") == "success":
            pattern_insights = patterns.get("insights", [])
            if pattern_insights:
                print(f"\n{self.colors['title']}Pattern Insights:{self.colors['reset']}")
                for i, insight in enumerate(pattern_insights):
                    print(f"  {i+1}. {insight}")
                all_insights.extend(pattern_insights)
        
        # Add correlation insights
        key_insights = correlations.get("key_insights", [])
        if key_insights:
            print(f"\n{self.colors['title']}Correlation Insights:{self.colors['reset']}")
            for i, insight in enumerate(key_insights):
                print(f"  {i+1}. {insight}")
            
            # Add only new insights (avoid duplicates)
            for insight in key_insights:
                if insight not in all_insights:
                    all_insights.append(insight)
        
        # Display recommendations based on insights
        if all_insights:
            print(f"\n{self.colors['title']}Recommendations:{self.colors['reset']}")
            recommendations = self._generate_recommendations(all_insights)
            for i, recommendation in enumerate(recommendations):
                print(f"  {i+1}. {recommendation}")
        else:
            print(f"\n{self.colors['warning']}No significant insights found. Try recording more varied data.{self.colors['reset']}")
        
        # Offer to show dashboard
        show_dashboard = input("\nWould you like to see a comprehensive dashboard visualization? (y/n): ").lower()
        if show_dashboard == 'y':
            print(f"\n{self.colors['cyan']}Generating dashboard... This may take a moment.{self.colors['reset']}")
            dashboard_path = self.visualization_generator.generate_dashboard(days=days)
            print(f"\n{self.colors['success']}Dashboard saved to: {dashboard_path}{self.colors['reset']}")
            print(f"Opening dashboard...")
            self._show_image(dashboard_path)
    
    def _settings_menu(self):
        """Display and handle the settings menu."""
        while True:
            print(f"\n{self.colors['title']}Settings Menu:{self.colors['reset']}")
            print(f"  1. {self.colors['cyan']}View Current Settings{self.colors['reset']}")
            print(f"  2. {self.colors['cyan']}Update Settings{self.colors['reset']}")
            print(f"  3. {self.colors['cyan']}Export Data{self.colors['reset']}")
            print(f"  4. {self.colors['cyan']}Import Data{self.colors['reset']}")
            print(f"  5. {self.colors['cyan']}Return to Main Menu{self.colors['reset']}")
            print()
            
            choice = input(f"{self.colors['prompt']}Enter your choice (1-5): {self.colors['reset']}")
            
            if choice == '1':
                self._view_settings()
            elif choice == '2':
                self._update_settings()
            elif choice == '3':
                self._export_data()
            elif choice == '4':
                self._import_data()
            elif choice == '5':
                break
            else:
                print(f"\n{self.colors['error']}Invalid choice. Please try again.{self.colors['reset']}\n")
    
    def _view_settings(self):
        """View current settings."""
        print(f"\n{self.colors['title']}Current Settings:{self.colors['reset']}")
        
        # Get user data
        user_data = self.data_collector.get_all_data()
        
        # Get settings
        settings = user_data.get("user_settings", {})
        
        # Display settings
        print(f"\n{self.colors['title']}Tracking Categories:{self.colors['reset']}")
        tracking_categories = settings.get("tracking_categories", [])
        for category in tracking_categories:
            print(f"  - {category}")
        
        print(f"\n{self.colors['title']}Mood Scale:{self.colors['reset']}")
        mood_scale = settings.get("mood_scale", {})
        print(f"  Min: {mood_scale.get('min', 1)}")
        print(f"  Max: {mood_scale.get('max', 10)}")
        
        labels = mood_scale.get("labels", {})
        if labels:
            print(f"  Labels:")
            for value, label in labels.items():
                print(f"    {value}: {label}")
        
        print(f"\n{self.colors['title']}Notification Preferences:{self.colors['reset']}")
        notifications = settings.get("notification_preferences", {})
        print(f"  Enabled: {notifications.get('enabled', True)}")
        print(f"  Frequency: {notifications.get('frequency', 'daily')}")
        print(f"  Time: {notifications.get('time', '20:00')}")
        
        print(f"\n{self.colors['title']}Data Storage:{self.colors['reset']}")
        print(f"  Data Directory: {self.data_dir}")
        print(f"  Visualization Directory: {self.output_dir}")
    
    def _update_settings(self):
        """Update settings."""
        print(f"\n{self.colors['title']}Update Settings:{self.colors['reset']}")
        
        # Get user data
        user_data = self.data_collector.get_all_data()
        
        # Get current settings
        settings = user_data.get("user_settings", {})
        
        # Display settings categories
        print(f"\nWhich settings would you like to update?")
        print(f"  1. {self.colors['cyan']}Tracking Categories{self.colors['reset']}")
        print(f"  2. {self.colors['cyan']}Mood Scale{self.colors['reset']}")
        print(f"  3. {self.colors['cyan']}Notification Preferences{self.colors['reset']}")
        print(f"  4. {self.colors['cyan']}Cancel{self.colors['reset']}")
        print()
        
        choice = input(f"{self.colors['prompt']}Enter your choice (1-4): {self.colors['reset']}")
        
        if choice == '1':
            # Update tracking categories
            current_categories = settings.get("tracking_categories", ["mood", "activities", "sleep"])
            print(f"\nCurrent tracking categories: {', '.join(current_categories)}")
            
            print(f"\nEnter new tracking categories (comma-separated):")
            print(f"Example: mood, activities, sleep, medication")
            
            categories_input = input("> ")
            if categories_input:
                new_categories = [c.strip() for c in categories_input.split(',')]
                settings["tracking_categories"] = new_categories
                
                # Update settings
                self.data_collector.update_settings(settings)
                print(f"\n{self.colors['success']}Tracking categories updated successfully!{self.colors['reset']}")
            else:
                print(f"\n{self.colors['warning']}No changes made to tracking categories.{self.colors['reset']}")
        
        elif choice == '2':
            # Update mood scale
            current_scale = settings.get("mood_scale", {
                "min": 1,
                "max": 10,
                "labels": {
                    "1": "Very Poor",
                    "5": "Neutral",
                    "10": "Excellent"
                }
            })
            
            print(f"\nCurrent mood scale:")
            print(f"  Min: {current_scale.get('min', 1)}")
            print(f"  Max: {current_scale.get('max', 10)}")
            
            # Update min/max
            min_input = input(f"\nEnter new minimum value (current: {current_scale.get('min', 1)}): ")
            if min_input:
                try:
                    min_value = int(min_input)
                    current_scale["min"] = min_value
                except ValueError:
                    print(f"{self.colors['error']}Invalid value. Using current minimum.{self.colors['reset']}")
            
            max_input = input(f"Enter new maximum value (current: {current_scale.get('max', 10)}): ")
            if max_input:
                try:
                    max_value = int(max_input)
                    current_scale["max"] = max_value
                except ValueError:
                    print(f"{self.colors['error']}Invalid value. Using current maximum.{self.colors['reset']}")
            
            # Update labels
            print(f"\nWould you like to update mood scale labels? (y/n): ")
            update_labels = input("> ").lower()
            
            if update_labels == 'y':
                labels = {}
                
                min_label = input(f"Enter label for minimum value ({current_scale['min']}): ")
                if min_label:
                    labels[str(current_scale['min'])] = min_label
                
                mid_label = input(f"Enter label for middle value ({(current_scale['min'] + current_scale['max']) // 2}): ")
                if mid_label:
                    labels[str((current_scale['min'] + current_scale['max']) // 2)] = mid_label
                
                max_label = input(f"Enter label for maximum value ({current_scale['max']}): ")
                if max_label:
                    labels[str(current_scale['max'])] = max_label
                
                if labels:
                    current_scale["labels"] = labels
            
            # Update settings
            settings["mood_scale"] = current_scale
            self.data_collector.update_settings(settings)
            print(f"\n{self.colors['success']}Mood scale updated successfully!{self.colors['reset']}")
        
        elif choice == '3':
            # Update notification preferences
            current_notifications = settings.get("notification_preferences", {
                "enabled": True,
                "frequency": "daily",
                "time": "20:00"
            })
            
            print(f"\nCurrent notification preferences:")
            print(f"  Enabled: {current_notifications.get('enabled', True)}")
            print(f"  Frequency: {current_notifications.get('frequency', 'daily')}")
            print(f"  Time: {current_notifications.get('time', '20:00')}")
            
            # Update enabled
            enabled_input = input(f"\nEnable notifications? (y/n, current: {'y' if current_notifications.get('enabled', True) else 'n'}): ").lower()
            if enabled_input in ['y', 'n']:
                current_notifications["enabled"] = (enabled_input == 'y')
            
            # Update frequency
            print(f"\nFrequency options: daily, twice_daily, weekly")
            frequency_input = input(f"Enter notification frequency (current: {current_notifications.get('frequency', 'daily')}): ")
            if frequency_input in ['daily', 'twice_daily', 'weekly']:
                current_notifications["frequency"] = frequency_input
            
            # Update time
            time_input = input(f"Enter notification time (HH:MM, current: {current_notifications.get('time', '20:00')}): ")
            if time_input:
                try:
                    # Validate time format
                    hour, minute = map(int, time_input.split(':'))
                    if 0 <= hour < 24 and 0 <= minute < 60:
                        current_notifications["time"] = time_input
                    else:
                        print(f"{self.colors['error']}Invalid time format. Using current time.{self.colors['reset']}")
                except (ValueError, TypeError):
                    print(f"{self.colors['error']}Invalid time format. Using current time.{self.colors['reset']}")
            
            # Update settings
            settings["notification_preferences"] = current_notifications
            self.data_collector.update_settings(settings)
            print(f"\n{self.colors['success']}Notification preferences updated successfully!{self.colors['reset']}")
        
        elif choice == '4':
            print(f"\n{self.colors['warning']}Settings update cancelled.{self.colors['reset']}")
        
        else:
            print(f"\n{self.colors['error']}Invalid choice. Settings update cancelled.{self.colors['reset']}")
    
    def _export_data(self):
        """Export user data."""
        print(f"\n{self.colors['title']}Export Data:{self.colors['reset']}")
        
        # Export data
        export_path = self.data_collector.export_data()
        
        print(f"\n{self.colors['success']}Data exported successfully to: {export_path}{self.colors['reset']}")
        print(f"You can copy this file to backup or transfer your data.")
    
    def _import_data(self):
        """Import user data."""
        print(f"\n{self.colors['title']}Import Data:{self.colors['reset']}")
        
        # Get import path
        import_path = input("Enter the path to the data file to import: ")
        
        if not os.path.exists(import_path):
            print(f"\n{self.colors['error']}File not found: {import_path}{self.colors['reset']}")
            return
        
        # Confirm import
        confirm = input(f"\n{self.colors['warning']}Warning: Importing data will replace your current data. Continue? (y/n): {self.colors['reset']}").lower()
        
        if confirm != 'y':
            print(f"\n{self.colors['warning']}Import cancelled.{self.colors['reset']}")
            return
        
        # Import data
        success = self.data_collector.import_data(import_path)
        
        if success:
            print(f"\n{self.colors['success']}Data imported successfully!{self.colors['reset']}")
        else:
            print(f"\n{self.colors['error']}Failed to import data. The file may be corrupted or in an invalid format.{self.colors['reset']}")
    
    def _show_recent_mood_history(self):
        """Show recent mood history."""
        print(f"\n{self.colors['title']}Recent Mood History:{self.colors['reset']}")
        
        # Get recent mood entries (last 7 days)
        mood_entries = self.mood_tracker.get_mood_history(days=7)
        
        if not mood_entries:
            print(f"{self.colors['warning']}No recent mood entries found.{self.colors['reset']}")
            return
        
        # Prepare data for display
        table_data = []
        for entry in mood_entries:
            timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M")
            
            emotions = ", ".join(entry.get("emotions", [])) if entry.get("emotions") else ""
            
            table_data.append([
                formatted_date,
                entry["mood_level"],
                emotions
            ])
        
        # Sort by date (most recent first)
        table_data.sort(reverse=True)
        
        # Display table
        headers = ["Date & Time", "Mood Level", "Emotions"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def _get_time_period(self):
        """Get time period from user."""
        print(f"\nSelect time period:")
        print(f"  1. Last 7 days")
        print(f"  2. Last 30 days")
        print(f"  3. Last 90 days")
        print(f"  4. Last 180 days")
        print(f"  5. Last 365 days")
        print(f"  6. Custom period")
        print()
        
        choice = input(f"{self.colors['prompt']}Enter your choice (1-6, default: 2): {self.colors['reset']}")
        
        if not choice:
            choice = '2'
        
        if choice == '1':
            return 7
        elif choice == '2':
            return 30
        elif choice == '3':
            return 90
        elif choice == '4':
            return 180
        elif choice == '5':
            return 365
        elif choice == '6':
            # Get custom period
            while True:
                try:
                    days = int(input("Enter number of days: "))
                    if days > 0:
                        return days
                    else:
                        print(f"{self.colors['error']}Please enter a positive number.{self.colors['reset']}")
                except ValueError:
                    print(f"{self.colors['error']}Please enter a valid number.{self.colors['reset']}")
        else:
            print(f"{self.colors['warning']}Invalid choice. Using default (30 days).{self.colors['reset']}")
            return 30
    
    def _get_entries_for_period(self, entry_type, days):
        """Get entries for a specific time period."""
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        return self.data_collector.get_entries_by_date_range(
            entry_type, 
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
    
    def _show_image(self, image_path):
        """Show an image using matplotlib."""
        try:
            img = plt.imread(image_path)
            plt.figure(figsize=(12, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"{self.colors['error']}Error displaying image: {str(e)}{self.colors['reset']}")
            print(f"Image saved to: {image_path}")
    
    def _generate_recommendations(self, insights):
        """Generate recommendations based on insights."""
        recommendations = []
        
        # Check for time of day patterns
        time_patterns = [insight for insight in insights if any(time in insight.lower() for time in ["morning", "afternoon", "evening"])]
        if time_patterns:
            for pattern in time_patterns:
                if "best" in pattern.lower():
                    time = None
                    for t in ["morning", "afternoon", "evening"]:
                        if t in pattern.lower():
                            time = t
                            break
                    
                    if time:
                        recommendations.append(f"Schedule important activities during the {time} when your mood tends to be better.")
        
        # Check for day of week patterns
        day_patterns = [insight for insight in insights if any(day in insight.lower() for day in ["weekday", "weekend", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])]
        if day_patterns:
            for pattern in day_patterns:
                if "better" in pattern.lower() and "weekend" in pattern.lower():
                    recommendations.append("Plan relaxing and enjoyable activities on weekends to maintain your positive mood.")
                elif "better" in pattern.lower() and "weekday" in pattern.lower():
                    recommendations.append("Leverage your positive weekday mood for productivity and challenging tasks.")
        
        # Check for activity correlations
        activity_patterns = [insight for insight in insights if "activity" in insight.lower() or "exercise" in insight.lower()]
        for pattern in activity_patterns:
            if "positive" in pattern.lower() and "exercise" in pattern.lower():
                recommendations.append("Consider incorporating more regular exercise into your routine to potentially improve your mood.")
            elif "positive" in pattern.lower():
                # Extract activity type
                activity = None
                words = pattern.split()
                for i, word in enumerate(words):
                    if word.lower() == "appears" and i > 0:
                        activity = words[i-1]
                        break
                
                if activity:
                    recommendations.append(f"Try to engage in more {activity.lower()} activities, as they appear to positively affect your mood.")
        
        # Check for sleep correlations
        sleep_patterns = [insight for insight in insights if "sleep" in insight.lower()]
        for pattern in sleep_patterns:
            if "optimal" in pattern.lower() or "best" in pattern.lower():
                # Try to extract optimal sleep duration
                import re
                duration_match = re.search(r'(\d+\.?\d*)\s*hours', pattern)
                if duration_match:
                    duration = duration_match.group(1)
                    recommendations.append(f"Aim for approximately {duration} hours of sleep for potentially better mood outcomes.")
            elif "quality" in pattern.lower() and "better" in pattern.lower():
                recommendations.append("Focus on improving sleep quality through good sleep hygiene practices.")
        
        # Check for mood cycles
        cycle_patterns = [insight for insight in insights if "cycle" in insight.lower()]
        for pattern in cycle_patterns:
            if "weekly" in pattern.lower():
                recommendations.append("Be mindful of your weekly mood patterns and plan activities accordingly.")
            elif "cycle" in pattern.lower():
                # Try to extract cycle length
                import re
                cycle_match = re.search(r'every\s*(\d+)\s*days', pattern)
                if cycle_match:
                    cycle_length = cycle_match.group(1)
                    recommendations.append(f"Your mood appears to cycle approximately every {cycle_length} days. Plan self-care activities proactively around these cycles.")
        
        # Check for trends
        trend_patterns = [insight for insight in insights if any(trend in insight.lower() for trend in ["improving", "declining", "stable"])]
        for pattern in trend_patterns:
            if "improving" in pattern.lower():
                recommendations.append("Your mood has been improving. Reflect on recent positive changes in your life and consider maintaining them.")
            elif "declining" in pattern.lower():
                recommendations.append("Your mood has been declining. Consider speaking with a mental health professional and reflecting on recent life changes.")
        
        # Add general recommendations if we don't have many specific ones
        if len(recommendations) < 3:
            general_recommendations = [
                "Consider tracking more varied activities to identify additional mood correlations.",
                "Regular mood tracking can help you better understand your emotional patterns.",
                "Experiment with different activities and observe their effects on your mood.",
                "Consistent sleep schedules often contribute to more stable mood patterns."
            ]
            
            # Add general recommendations until we have at least 3
            for rec in general_recommendations:
                if rec not in recommendations:
                    recommendations.append(rec)
                    if len(recommendations) >= 3:
                        break
        
        return recommendations


def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="Mental Health Pattern Recognition Assistant")
    parser.add_argument("--data-dir", default="../data", help="Directory for data storage")
    parser.add_argument("--output-dir", default="../visualization", help="Directory for visualization output")
    
    args = parser.parse_args()
    
    # Create and run the user interface
    ui = UserInterface(data_dir=args.data_dir, output_dir=args.output_dir)
    ui.run()


if __name__ == "__main__":
    main()
