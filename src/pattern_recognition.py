"""
Pattern Recognition Engine for Mental Health Pattern Recognition Assistant

This module provides functionality for identifying patterns and correlations
in mental health data, including mood, activities, sleep, and other factors.
"""

import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import pearsonr
from src.data_collection import DataCollector

class PatternRecognitionEngine:
    """
    Analyzes mental health data to identify patterns, correlations, and insights.
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize the pattern recognition engine with a data collector.
        
        Args:
            data_collector: Optional DataCollector instance, creates a new one if None
        """
        self.data_collector = data_collector or DataCollector()
        
    def _prepare_dataframe(self, days: int = 90) -> pd.DataFrame:
        """
        Prepare a pandas DataFrame from collected data for analysis.
        
        Args:
            days: Number of days of data to include
            
        Returns:
            DataFrame with all relevant data points
        """
        # Calculate date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Get data from collector
        mood_entries = self.data_collector.get_entries_by_date_range(
            "mood_entries", 
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        activity_entries = self.data_collector.get_entries_by_date_range(
            "activity_entries", 
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        sleep_entries = self.data_collector.get_entries_by_date_range(
            "sleep_entries", 
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Convert to DataFrame
        mood_df = pd.DataFrame(mood_entries)
        activity_df = pd.DataFrame(activity_entries)
        sleep_df = pd.DataFrame(sleep_entries)
        
        # If any dataframe is empty, create with columns to avoid errors
        if mood_df.empty:
            mood_df = pd.DataFrame(columns=["timestamp", "mood_level", "emotions", "notes"])
        
        if activity_df.empty:
            activity_df = pd.DataFrame(columns=["timestamp", "activity_type", "duration_minutes", "intensity", "notes"])
        
        if sleep_df.empty:
            sleep_df = pd.DataFrame(columns=["timestamp", "duration_hours", "quality", "notes"])
        
        # Convert timestamps to datetime
        for df in [mood_df, activity_df, sleep_df]:
            if not df.empty and "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df["date"] = df["timestamp"].dt.date
        
        # Return the dataframes
        return {
            "mood": mood_df,
            "activity": activity_df,
            "sleep": sleep_df
        }
    
    def identify_mood_patterns(self, days: int = 90) -> Dict[str, Any]:
        """
        Identify patterns in mood data.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with identified patterns and insights
        """
        dataframes = self._prepare_dataframe(days)
        mood_df = dataframes["mood"]
        
        if mood_df.empty or len(mood_df) < 5:
            return {
                "status": "insufficient_data",
                "message": "Not enough mood data to identify patterns"
            }
        
        # Analyze daily patterns
        mood_df["hour"] = mood_df["timestamp"].dt.hour
        mood_df["day_of_week"] = mood_df["timestamp"].dt.dayofweek
        
        # Time of day patterns
        morning_mood = mood_df[mood_df["hour"].between(5, 11)]["mood_level"].mean() if not mood_df[mood_df["hour"].between(5, 11)].empty else None
        afternoon_mood = mood_df[mood_df["hour"].between(12, 17)]["mood_level"].mean() if not mood_df[mood_df["hour"].between(12, 17)].empty else None
        evening_mood = mood_df[mood_df["hour"].between(18, 23)]["mood_level"].mean() if not mood_df[mood_df["hour"].between(18, 23)].empty else None
        
        # Day of week patterns
        weekday_mood = mood_df[mood_df["day_of_week"] < 5]["mood_level"].mean() if not mood_df[mood_df["day_of_week"] < 5].empty else None
        weekend_mood = mood_df[mood_df["day_of_week"] >= 5]["mood_level"].mean() if not mood_df[mood_df["day_of_week"] >= 5].empty else None
        
        # Trend analysis
        mood_df_sorted = mood_df.sort_values("timestamp")
        mood_values = mood_df_sorted["mood_level"].values
        
        # Check if we have enough data for trend analysis
        trend_data = {}
        if len(mood_values) >= 7:
            # Simple linear trend
            x = np.arange(len(mood_values))
            coeffs = np.polyfit(x, mood_values, 1)
            trend = coeffs[0]  # Slope of the trend line
            
            # Weekly average trend
            if len(mood_values) >= 14:
                weekly_means = []
                for i in range(0, len(mood_values), 7):
                    if i + 7 <= len(mood_values):
                        weekly_means.append(np.mean(mood_values[i:i+7]))
                
                if len(weekly_means) >= 2:
                    weekly_x = np.arange(len(weekly_means))
                    weekly_coeffs = np.polyfit(weekly_x, weekly_means, 1)
                    weekly_trend = weekly_coeffs[0]
                    trend_data["weekly_trend"] = float(weekly_trend)
                    trend_data["weekly_direction"] = "improving" if weekly_trend > 0.1 else "declining" if weekly_trend < -0.1 else "stable"
            
            trend_data["overall_trend"] = float(trend)
            trend_data["direction"] = "improving" if trend > 0.05 else "declining" if trend < -0.05 else "stable"
        
        # Compile results
        patterns = {
            "status": "success",
            "time_of_day": {
                "morning": float(morning_mood) if morning_mood is not None else None,
                "afternoon": float(afternoon_mood) if afternoon_mood is not None else None,
                "evening": float(evening_mood) if evening_mood is not None else None,
                "best_time": self._get_best_time_of_day(morning_mood, afternoon_mood, evening_mood)
            },
            "day_of_week": {
                "weekday": float(weekday_mood) if weekday_mood is not None else None,
                "weekend": float(weekend_mood) if weekend_mood is not None else None,
                "better_period": "weekends" if weekend_mood is not None and weekday_mood is not None and weekend_mood > weekday_mood + 0.5 else
                               "weekdays" if weekday_mood is not None and weekend_mood is not None and weekday_mood > weekend_mood + 0.5 else
                               "similar"
            },
            "trend_analysis": trend_data
        }
        
        # Generate insights
        insights = []
        
        # Time of day insights
        if patterns["time_of_day"]["best_time"]:
            insights.append(f"Your mood tends to be best during the {patterns['time_of_day']['best_time']}.")
        
        # Day of week insights
        if patterns["day_of_week"]["better_period"] == "weekends":
            insights.append("Your mood is typically better on weekends compared to weekdays.")
        elif patterns["day_of_week"]["better_period"] == "weekdays":
            insights.append("Your mood is typically better on weekdays compared to weekends.")
        
        # Trend insights
        if "direction" in trend_data:
            if trend_data["direction"] == "improving":
                insights.append("Your overall mood has been improving during this period.")
            elif trend_data["direction"] == "declining":
                insights.append("Your overall mood has been declining during this period.")
            else:
                insights.append("Your overall mood has been relatively stable during this period.")
        
        patterns["insights"] = insights
        return patterns
    
    def _get_best_time_of_day(self, morning, afternoon, evening):
        """Helper to determine best time of day based on mood averages."""
        times = []
        if morning is not None:
            times.append(("morning", morning))
        if afternoon is not None:
            times.append(("afternoon", afternoon))
        if evening is not None:
            times.append(("evening", evening))
        
        if not times:
            return None
            
        best_time = max(times, key=lambda x: x[1])
        
        # Only return if there's a meaningful difference
        threshold = 0.5
        if any(best_time[1] - value > threshold for name, value in times if name != best_time[0]):
            return best_time[0]
        return None
    
    def identify_activity_mood_correlations(self, days: int = 90) -> Dict[str, Any]:
        """
        Identify correlations between activities and mood.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with identified correlations and insights
        """
        dataframes = self._prepare_dataframe(days)
        mood_df = dataframes["mood"]
        activity_df = dataframes["activity"]
        
        if mood_df.empty or activity_df.empty or len(mood_df) < 5 or len(activity_df) < 5:
            return {
                "status": "insufficient_data",
                "message": "Not enough data to identify activity-mood correlations"
            }
        
        # Aggregate by date
        daily_mood = mood_df.groupby("date")["mood_level"].mean().reset_index()
        
        # Create activity features
        activity_types = activity_df["activity_type"].unique()
        activity_features = {}
        
        for activity in activity_types:
            # Filter for this activity
            activity_data = activity_df[activity_df["activity_type"] == activity]
            
            # Aggregate by date
            daily_activity = activity_data.groupby("date").agg({
                "duration_minutes": "sum",
                "intensity": "mean"
            }).reset_index()
            
            # Store in features dict
            activity_features[activity] = daily_activity
        
        # Calculate correlations
        correlations = []
        
        for activity, activity_data in activity_features.items():
            # Merge with mood data
            merged = pd.merge(daily_mood, activity_data, on="date", how="inner")
            
            if len(merged) < 5:
                continue
                
            # Calculate correlation between duration and mood
            duration_corr, duration_p = pearsonr(merged["duration_minutes"], merged["mood_level"])
            
            # Calculate correlation between intensity and mood if available
            intensity_corr = None
            intensity_p = None
            if "intensity" in merged.columns and not merged["intensity"].isna().all():
                intensity_corr, intensity_p = pearsonr(
                    merged["intensity"].fillna(merged["intensity"].mean()), 
                    merged["mood_level"]
                )
            
            correlations.append({
                "activity": activity,
                "duration_correlation": float(duration_corr),
                "duration_p_value": float(duration_p),
                "duration_significance": duration_p < 0.05,
                "intensity_correlation": float(intensity_corr) if intensity_corr is not None else None,
                "intensity_p_value": float(intensity_p) if intensity_p is not None else None,
                "intensity_significance": intensity_p < 0.05 if intensity_p is not None else None,
                "sample_size": len(merged)
            })
        
        # Sort by correlation strength
        correlations.sort(key=lambda x: abs(x["duration_correlation"]), reverse=True)
        
        # Generate insights
        insights = []
        
        for corr in correlations:
            if corr["duration_significance"]:
                if corr["duration_correlation"] > 0.3:
                    insights.append(f"{corr['activity']} appears to have a positive effect on your mood.")
                elif corr["duration_correlation"] < -0.3:
                    insights.append(f"{corr['activity']} appears to have a negative association with your mood.")
        
        return {
            "status": "success",
            "correlations": correlations,
            "insights": insights
        }
    
    def identify_sleep_mood_correlations(self, days: int = 90) -> Dict[str, Any]:
        """
        Identify correlations between sleep and mood.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with identified correlations and insights
        """
        dataframes = self._prepare_dataframe(days)
        mood_df = dataframes["mood"]
        sleep_df = dataframes["sleep"]
        
        if mood_df.empty or sleep_df.empty or len(mood_df) < 5 or len(sleep_df) < 5:
            return {
                "status": "insufficient_data",
                "message": "Not enough data to identify sleep-mood correlations"
            }
        
        # Aggregate by date
        daily_mood = mood_df.groupby("date")["mood_level"].mean().reset_index()
        daily_sleep = sleep_df.groupby("date").agg({
            "duration_hours": "mean",
            "quality": "mean"
        }).reset_index()
        
        # Merge datasets
        merged = pd.merge(daily_mood, daily_sleep, on="date", how="inner")
        
        if len(merged) < 5:
            return {
                "status": "insufficient_data",
                "message": "Not enough matching dates between sleep and mood data"
            }
        
        # Calculate correlations
        duration_corr, duration_p = pearsonr(merged["duration_hours"], merged["mood_level"])
        
        quality_corr = None
        quality_p = None
        if "quality" in merged.columns and not merged["quality"].isna().all():
            quality_corr, quality_p = pearsonr(
                merged["quality"].fillna(merged["quality"].mean()), 
                merged["mood_level"]
            )
        
        # Find optimal sleep duration
        if len(merged) >= 10:
            # Group by sleep duration rounded to nearest half hour
            merged["duration_rounded"] = (merged["duration_hours"] * 2).round() / 2
            sleep_groups = merged.groupby("duration_rounded")["mood_level"].mean().reset_index()
            
            if len(sleep_groups) >= 3:
                optimal_duration = sleep_groups.loc[sleep_groups["mood_level"].idxmax(), "duration_rounded"]
            else:
                optimal_duration = None
        else:
            optimal_duration = None
        
        # Generate insights
        insights = []
        
        if duration_p < 0.05:
            if duration_corr > 0.3:
                insights.append("More sleep appears to positively affect your mood.")
            elif duration_corr < -0.3:
                insights.append("Longer sleep duration appears to negatively affect your mood, which is unusual. Consider other factors like sleep quality or oversleeping.")
        
        if quality_p is not None and quality_p < 0.05 and quality_corr > 0.3:
            insights.append("Better sleep quality is associated with improved mood.")
        
        if optimal_duration is not None:
            insights.append(f"Your mood tends to be best when you sleep around {optimal_duration} hours.")
        
        return {
            "status": "success",
            "correlations": {
                "duration": {
                    "correlation": float(duration_corr),
                    "p_value": float(duration_p),
                    "significant": duration_p < 0.05
                },
                "quality": {
                    "correlation": float(quality_corr) if quality_corr is not None else None,
                    "p_value": float(quality_p) if quality_p is not None else None,
                    "significant": quality_p < 0.05 if quality_p is not None else None
                }
            },
            "optimal_sleep_duration": float(optimal_duration) if optimal_duration is not None else None,
            "insights": insights
        }
    
    def identify_mood_clusters(self, days: int = 90) -> Dict[str, Any]:
        """
        Identify distinct mood patterns using clustering.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with identified clusters and insights
        """
        dataframes = self._prepare_dataframe(days)
        mood_df = dataframes["mood"]
        
        if mood_df.empty or len(mood_df) < 10:
            return {
                "status": "insufficient_data",
                "message": "Not enough mood data for clustering analysis"
            }
        
        # Extract features for clustering
        features = []
        
        # Add mood level
        features.append(mood_df["mood_level"].values.reshape(-1, 1))
        
        # Add time of day (hour)
        if "timestamp" in mood_df.columns:
            hour_feature = mood_df["timestamp"].dt.hour.values.reshape(-1, 1)
            features.append(hour_feature)
        
        # Add day of week
        if "timestamp" in mood_df.columns:
            day_feature = mood_df["timestamp"].dt.dayofweek.values.reshape(-1, 1)
            features.append(day_feature)
        
        # Combine features
        X = np.hstack(features)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Determine optimal number of clusters (2-4)
        max_clusters = min(4, len(mood_df) // 3)
        if max_clusters < 2:
            max_clusters = 2
            
        inertias = []
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
        
        # Find elbow point or use 2 clusters as default
        if len(inertias) > 1:
            # Calculate rate of change in inertia
            inertia_changes = [inertias[i-1] - inertias[i] for i in range(1, len(inertias))]
            
            # Find where the rate of change slows down significantly
            optimal_k = 2
            for i, change in enumerate(inertia_changes):
                if i > 0 and change < 0.5 * inertia_changes[i-1]:
                    optimal_k = i + 2  # +2 because we started with k=2
                    break
        else:
            optimal_k = 2
        
        # Perform clustering with optimal k
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to dataframe
        mood_df = mood_df.copy()
        mood_df["cluster"] = clusters
        
        # Analyze clusters
        cluster_stats = []
        for i in range(optimal_k):
            cluster_data = mood_df[mood_df["cluster"] == i]
            
            # Basic statistics
            avg_mood = cluster_data["mood_level"].mean()
            
            # Time patterns
            if "timestamp" in cluster_data.columns:
                avg_hour = cluster_data["timestamp"].dt.hour.mean()
                day_counts = cluster_data["timestamp"].dt.dayofweek.value_counts()
                most_common_day = day_counts.idxmax()
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                most_common_day_name = day_names[most_common_day]
            else:
                avg_hour = None
                most_common_day_name = None
            
            # Emotion analysis
            common_emotions = []
            if "emotions" in cluster_data.columns:
                all_emotions = []
                for emotions_list in cluster_data["emotions"]:
                    if emotions_list:
                        all_emotions.extend(emotions_list)
                
                if all_emotions:
                    emotion_counts = {}
                    for emotion in all_emotions:
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    
                    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
                    common_emotions = [emotion for emotion, count in sorted_emotions[:3]]
            
            # Determine cluster characteristics
            time_of_day = None
            if avg_hour is not None:
                if 5 <= avg_hour < 12:
                    time_of_day = "morning"
                elif 12 <= avg_hour < 18:
                    time_of_day = "afternoon"
                else:
                    time_of_day = "evening"
            
            mood_category = None
            if avg_mood >= 7:
                mood_category = "positive"
            elif avg_mood <= 4:
                mood_category = "negative"
            else:
                mood_category = "neutral"
            
            cluster_stats.append({
                "cluster_id": i,
                "size": len(cluster_data),
                "percentage": (len(cluster_data) / len(mood_df)) * 100,
                "avg_mood": float(avg_mood),
                "mood_category": mood_category,
                "time_of_day": time_of_day,
                "most_common_day": most_common_day_name,
                "common_emotions": common_emotions
            })
        
        # Generate insights
        insights = []
        
        for cluster in cluster_stats:
            description = f"Cluster {cluster['cluster_id']+1} ({cluster['percentage']:.1f}% of entries): "
            
            characteristics = []
            if cluster["mood_category"]:
                characteristics.append(f"{cluster['mood_category']} mood")
            
            if cluster["time_of_day"]:
                characteristics.append(f"{cluster['time_of_day']} entries")
            
            if cluster["most_common_day"]:
                characteristics.append(f"often on {cluster['most_common_day']}")
            
            if cluster["common_emotions"]:
                emotions_str = ", ".join(cluster["common_emotions"])
                characteristics.append(f"emotions: {emotions_str}")
            
            description += ", ".join(characteristics)
            insights.append(description)
        
        return {
            "status": "success",
            "optimal_clusters": optimal_k,
            "cluster_stats": cluster_stats,
            "insights": insights
        }
    
    def generate_comprehensive_analysis(self, days: int = 90) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis of all patterns and correlations.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with all analyses and insights
        """
        # Run all analyses
        mood_patterns = self.identify_mood_patterns(days)
        activity_correlations = self.identify_activity_mood_correlations(days)
        sleep_correlations = self.identify_sleep_mood_correlations(days)
        mood_clusters = self.identify_mood_clusters(days)
        
        # Compile all insights
        all_insights = []
        
        if mood_patterns.get("status") == "success":
            all_insights.extend(mood_patterns.get("insights", []))
        
        if activity_correlations.get("status") == "success":
            all_insights.extend(activity_correlations.get("insights", []))
        
        if sleep_correlations.get("status") == "success":
            all_insights.extend(sleep_correlations.get("insights", []))
        
        if mood_clusters.get("status") == "success":
            all_insights.extend(mood_clusters.get("insights", []))
        
        # Compile results
        return {
            "mood_patterns": mood_patterns,
            "activity_correlations": activity_correlations,
            "sleep_correlations": sleep_correlations,
            "mood_clusters": mood_clusters,
            "key_insights": all_insights
        }


# Example usage
if __name__ == "__main__":
    from src.data_collection import DataCollector
    
    # Create data collector and add sample data
    collector = DataCollector()
    
    # Add some sample data spanning multiple days
    for i in range(30):
        # Create a date i days ago
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        
        # Morning entry
        morning = date.replace(hour=8, minute=0, second=0)
        # Evening entry
        evening = date.replace(hour=20, minute=0, second=0)
        
        # Add mood entries with some patterns
        # Weekday pattern: lower mood on weekdays
        is_weekend = date.weekday() >= 5
        base_mood = 7 if is_weekend else 5
        
        # Add some random variation
        morning_mood = max(1, min(10, base_mood + np.random.randint(-1, 2)))
        evening_mood = max(1, min(10, base_mood + np.random.randint(-1, 2)))
        
        # Record moods
        collector.record_mood(
            mood_level=morning_mood,
            notes="Morning entry",
            emotions=["calm"] if morning_mood > 5 else ["tired"],
            timestamp=morning.isoformat()
        )
        
        collector.record_mood(
            mood_level=evening_mood,
            notes="Evening entry",
            emotions=["relaxed"] if evening_mood > 5 else ["stressed"],
            timestamp=evening.isoformat()
        )
        
        # Add activity entries
        if i % 3 == 0:  # Every 3 days
            collector.record_activity(
                activity_type="exercise",
                duration_minutes=30,
                intensity=4,
                notes="Workout",
                timestamp=date.replace(hour=18).isoformat()
            )
        
        # Add sleep entries
        sleep_duration = 8 if is_weekend else 6.5
        collector.record_sleep(
            duration_hours=sleep_duration,
            quality=7 if sleep_duration >= 7.5 else 5,
            notes="Sleep record",
            start_time=date.replace(hour=23).isoformat(),
            end_time=date.replace(hour=7).isoformat()
        )
    
    # Create pattern recognition engine and analyze
    engine = PatternRecognitionEngine(collector)
    analysis = engine.generate_comprehensive_analysis()
    
    # Print key insights
    print("Key Insights:")
    for i, insight in enumerate(analysis["key_insights"]):
        print(f"{i+1}. {insight}")
