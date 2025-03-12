"""
Mood Tracking Module for Mental Health Pattern Recognition Assistant

This module provides functionality for tracking, analyzing, and visualizing mood data.
It builds on the data collection module to provide specific mood-related features.
"""

import datetime
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
from src.data_collection import DataCollector

class MoodTracker:
    """
    Handles mood tracking, analysis, and visualization functionality.
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize the mood tracker with a data collector.
        
        Args:
            data_collector: Optional DataCollector instance, creates a new one if None
        """
        self.data_collector = data_collector or DataCollector()
        self.emotion_categories = {
            "positive": ["happy", "content", "excited", "grateful", "relaxed", "peaceful", 
                        "optimistic", "confident", "inspired", "proud"],
            "negative": ["sad", "anxious", "stressed", "angry", "frustrated", "overwhelmed", 
                        "irritated", "disappointed", "worried", "fearful"],
            "neutral": ["calm", "focused", "contemplative", "curious", "surprised", 
                       "nostalgic", "reflective", "alert", "determined"]
        }
    
    def log_mood(self, 
                mood_level: int, 
                notes: Optional[str] = None,
                emotions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Log a mood entry with the current timestamp.
        
        Args:
            mood_level: Numerical mood rating (typically 1-10)
            notes: Optional text notes about the mood
            emotions: Optional list of specific emotions experienced
            
        Returns:
            The created mood entry
        """
        return self.data_collector.record_mood(
            mood_level=mood_level,
            notes=notes,
            emotions=emotions
        )
    
    def get_mood_history(self, 
                        days: Optional[int] = None, 
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get mood history for a specified period.
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            List of mood entries within the specified period
        """
        if days is not None:
            # Calculate start date based on days
            end = datetime.datetime.now()
            start = end - datetime.timedelta(days=days)
            start_date = start.isoformat()
            end_date = end.isoformat()
            
        return self.data_collector.get_entries_by_date_range(
            entry_type="mood_entries",
            start_date=start_date,
            end_date=end_date
        )
    
    def get_average_mood(self, 
                        days: Optional[int] = None,
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> float:
        """
        Calculate average mood level for a specified period.
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            Average mood level or 0 if no entries
        """
        mood_entries = self.get_mood_history(days, start_date, end_date)
        
        if not mood_entries:
            return 0
            
        total_mood = sum(entry["mood_level"] for entry in mood_entries)
        return total_mood / len(mood_entries)
    
    def get_mood_range(self, 
                      days: Optional[int] = None,
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> Tuple[int, int]:
        """
        Get the range of mood levels for a specified period.
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            Tuple of (min_mood, max_mood) or (0, 0) if no entries
        """
        mood_entries = self.get_mood_history(days, start_date, end_date)
        
        if not mood_entries:
            return (0, 0)
            
        mood_levels = [entry["mood_level"] for entry in mood_entries]
        return (min(mood_levels), max(mood_levels))
    
    def get_mood_volatility(self, 
                           days: Optional[int] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> float:
        """
        Calculate mood volatility (standard deviation) for a specified period.
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            Standard deviation of mood levels or 0 if fewer than 2 entries
        """
        mood_entries = self.get_mood_history(days, start_date, end_date)
        
        if len(mood_entries) < 2:
            return 0
            
        mood_levels = [entry["mood_level"] for entry in mood_entries]
        return np.std(mood_levels)
    
    def get_common_emotions(self, 
                           days: Optional[int] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           limit: int = 5) -> List[Tuple[str, int]]:
        """
        Get most common emotions for a specified period.
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            limit: Maximum number of emotions to return
            
        Returns:
            List of (emotion, count) tuples, sorted by count descending
        """
        mood_entries = self.get_mood_history(days, start_date, end_date)
        
        if not mood_entries:
            return []
            
        # Count emotions
        emotion_counts = {}
        for entry in mood_entries:
            if entry.get("emotions"):
                for emotion in entry["emotions"]:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Sort by count and limit
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions[:limit]
    
    def get_emotion_category_distribution(self, 
                                         days: Optional[int] = None,
                                         start_date: Optional[str] = None,
                                         end_date: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate distribution of emotion categories (positive, negative, neutral).
        
        Args:
            days: Optional number of days to look back
            start_date: Optional start date in ISO format
            end_date: Optional end date in ISO format
            
        Returns:
            Dictionary with category percentages
        """
        mood_entries = self.get_mood_history(days, start_date, end_date)
        
        if not mood_entries:
            return {"positive": 0, "negative": 0, "neutral": 0, "uncategorized": 0}
        
        # Initialize counters
        category_counts = {"positive": 0, "negative": 0, "neutral": 0, "uncategorized": 0}
        total_emotions = 0
        
        # Count emotions by category
        for entry in mood_entries:
            if entry.get("emotions"):
                for emotion in entry["emotions"]:
                    categorized = False
                    for category, emotions in self.emotion_categories.items():
                        if emotion.lower() in emotions:
                            category_counts[category] += 1
                            categorized = True
                            break
                    
                    if not categorized:
                        category_counts["uncategorized"] += 1
                    
                    total_emotions += 1
        
        # Calculate percentages
        if total_emotions > 0:
            return {category: (count / total_emotions) * 100 
                   for category, count in category_counts.items()}
        else:
            return {category: 0 for category in category_counts}
    
    def plot_mood_timeline(self, 
                          days: int = 30,
                          save_path: Optional[str] = None) -> str:
        """
        Generate a timeline plot of mood levels.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the plot image
            
        Returns:
            Path to saved plot or empty string if plotting failed
        """
        mood_entries = self.get_mood_history(days=days)
        
        if not mood_entries:
            return ""
        
        # Sort entries by timestamp
        mood_entries.sort(key=lambda x: x["timestamp"])
        
        # Extract dates and mood levels
        dates = [datetime.datetime.fromisoformat(entry["timestamp"]).date() for entry in mood_entries]
        mood_levels = [entry["mood_level"] for entry in mood_entries]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(dates, mood_levels, 'o-', color='#3498db')
        plt.axhline(y=np.mean(mood_levels), color='#e74c3c', linestyle='--', alpha=0.7, 
                   label=f'Average: {np.mean(mood_levels):.1f}')
        
        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Mood Level')
        plt.title(f'Mood Timeline - Last {days} Days')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Adjust layout and save
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            temp_path = "../data/mood_timeline.png"
            plt.savefig(temp_path)
            plt.close()
            return temp_path
    
    def plot_emotion_distribution(self, 
                                days: int = 30,
                                save_path: Optional[str] = None) -> str:
        """
        Generate a pie chart of emotion category distribution.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the plot image
            
        Returns:
            Path to saved plot or empty string if plotting failed
        """
        distribution = self.get_emotion_category_distribution(days=days)
        
        # Filter out zero values
        distribution = {k: v for k, v in distribution.items() if v > 0}
        
        if not distribution:
            return ""
        
        # Create color map
        colors = {
            "positive": "#2ecc71",  # Green
            "negative": "#e74c3c",  # Red
            "neutral": "#3498db",   # Blue
            "uncategorized": "#95a5a6"  # Gray
        }
        
        # Create plot
        plt.figure(figsize=(10, 7))
        plt.pie(
            distribution.values(), 
            labels=distribution.keys(),
            autopct='%1.1f%%',
            colors=[colors.get(category, "#95a5a6") for category in distribution.keys()],
            startangle=90,
            shadow=False
        )
        
        # Add title
        plt.title(f'Emotion Distribution - Last {days} Days')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Save plot
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            temp_path = "../data/emotion_distribution.png"
            plt.savefig(temp_path)
            plt.close()
            return temp_path
    
    def generate_mood_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of mood data.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dictionary with mood summary statistics and insights
        """
        mood_entries = self.get_mood_history(days=days)
        
        if not mood_entries:
            return {
                "status": "insufficient_data",
                "message": f"No mood data available for the last {days} days"
            }
        
        # Calculate basic statistics
        mood_levels = [entry["mood_level"] for entry in mood_entries]
        avg_mood = np.mean(mood_levels)
        min_mood, max_mood = min(mood_levels), max(mood_levels)
        volatility = np.std(mood_levels)
        
        # Get emotion data
        common_emotions = self.get_common_emotions(days=days)
        emotion_distribution = self.get_emotion_category_distribution(days=days)
        
        # Generate plots
        timeline_plot = self.plot_mood_timeline(days=days)
        emotion_plot = self.plot_emotion_distribution(days=days)
        
        # Compile summary
        summary = {
            "status": "success",
            "period_days": days,
            "entry_count": len(mood_entries),
            "statistics": {
                "average_mood": float(avg_mood),
                "mood_range": [int(min_mood), int(max_mood)],
                "mood_volatility": float(volatility)
            },
            "emotions": {
                "common_emotions": common_emotions,
                "category_distribution": emotion_distribution
            },
            "visualizations": {
                "timeline_plot": timeline_plot,
                "emotion_plot": emotion_plot
            }
        }
        
        # Add basic insights
        insights = []
        
        # Mood trend insight
        if len(mood_entries) >= 7:
            recent_mood = np.mean([entry["mood_level"] for entry in mood_entries[-3:]])
            earlier_mood = np.mean([entry["mood_level"] for entry in mood_entries[:3]])
            
            if recent_mood > earlier_mood + 1:
                insights.append("Your mood has been improving over this period.")
            elif recent_mood < earlier_mood - 1:
                insights.append("Your mood has been declining over this period.")
            else:
                insights.append("Your mood has been relatively stable over this period.")
        
        # Volatility insight
        if volatility > 2.5:
            insights.append("Your mood shows significant fluctuation, which may be worth exploring.")
        elif volatility < 1.0:
            insights.append("Your mood shows very little variation, which can be either positive stability or emotional blunting.")
        
        # Emotion insight
        if emotion_distribution.get("positive", 0) > 60:
            insights.append("You're experiencing predominantly positive emotions.")
        elif emotion_distribution.get("negative", 0) > 60:
            insights.append("You're experiencing predominantly negative emotions.")
        
        summary["insights"] = insights
        return summary


# Example usage
if __name__ == "__main__":
    tracker = MoodTracker()
    
    # Log some sample moods
    tracker.log_mood(7, "Feeling good today", ["happy", "relaxed"])
    tracker.log_mood(4, "Stressed about work", ["anxious", "overwhelmed"])
    tracker.log_mood(6, "Mixed feelings", ["hopeful", "worried"])
    
    # Generate and print summary
    summary = tracker.generate_mood_summary(days=7)
    print(f"Average mood: {summary['statistics']['average_mood']:.1f}")
    print(f"Mood range: {summary['statistics']['mood_range']}")
    print(f"Common emotions: {summary['emotions']['common_emotions']}")
    print(f"Insights: {summary['insights']}")
