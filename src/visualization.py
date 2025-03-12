"""
Visualization Component for Mental Health Pattern Recognition Assistant

This module provides visualization functionality for displaying mood patterns,
correlations, and insights in an intuitive and informative way.
"""

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
import os
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from src.data_collection import DataCollector

class VisualizationGenerator:
    """
    Generates visualizations for mental health data patterns and insights.
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None, output_dir: str = "../visualization"):
        """
        Initialize the visualization generator with a data collector.
        
        Args:
            data_collector: Optional DataCollector instance, creates a new one if None
            output_dir: Directory to save visualization files
        """
        self.data_collector = data_collector or DataCollector()
        self.output_dir = output_dir
        self.ensure_output_directory()
        
        # Set up color schemes
        self.mood_colors = {
            "high": "#2ecc71",  # Green
            "medium": "#3498db",  # Blue
            "low": "#e74c3c"    # Red
        }
        
        # Create custom color maps
        self.mood_cmap = LinearSegmentedColormap.from_list(
            "mood_cmap", 
            [self.mood_colors["low"], self.mood_colors["medium"], self.mood_colors["high"]]
        )
        
        # Set default style
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _prepare_daily_dataframe(self, days: int = 90) -> pd.DataFrame:
        """
        Prepare a daily aggregated DataFrame from collected data for visualization.
        
        Args:
            days: Number of days of data to include
            
        Returns:
            DataFrame with daily aggregated data
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
        mood_df = pd.DataFrame(mood_entries) if mood_entries else pd.DataFrame()
        activity_df = pd.DataFrame(activity_entries) if activity_entries else pd.DataFrame()
        sleep_df = pd.DataFrame(sleep_entries) if sleep_entries else pd.DataFrame()
        
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
        
        # Aggregate mood data by day
        daily_mood = None
        if not mood_df.empty:
            daily_mood = mood_df.groupby("date")["mood_level"].agg(['mean', 'min', 'max', 'count']).reset_index()
            daily_mood.columns = ["date", "mood_mean", "mood_min", "mood_max", "mood_count"]
        
        # Aggregate activity data by day and type
        daily_activity = None
        if not activity_df.empty and len(activity_df) > 0:
            # Get unique activity types
            activity_types = activity_df["activity_type"].unique()
            
            # Create activity features for each type
            activity_dfs = []
            
            for activity in activity_types:
                # Filter for this activity
                activity_data = activity_df[activity_df["activity_type"] == activity]
                
                # Aggregate by date
                agg_data = activity_data.groupby("date").agg({
                    "duration_minutes": "sum",
                    "intensity": "mean"
                }).reset_index()
                
                # Rename columns to include activity type
                agg_data.columns = ["date", f"{activity}_duration", f"{activity}_intensity"]
                
                # Replace NaN with 0 for intensity
                agg_data[f"{activity}_intensity"] = agg_data[f"{activity}_intensity"].fillna(0)
                
                activity_dfs.append(agg_data)
            
            # Merge all activity dataframes
            if activity_dfs:
                daily_activity = activity_dfs[0]
                for df in activity_dfs[1:]:
                    daily_activity = pd.merge(daily_activity, df, on="date", how="outer")
        
        # Aggregate sleep data by day
        daily_sleep = None
        if not sleep_df.empty:
            daily_sleep = sleep_df.groupby("date").agg({
                "duration_hours": "mean",
                "quality": "mean"
            }).reset_index()
            daily_sleep.columns = ["date", "sleep_duration", "sleep_quality"]
        
        # Create a date range for all days
        date_range = pd.DataFrame({
            "date": pd.date_range(start=start_date.date(), end=end_date.date())
        })
        date_range["date"] = date_range["date"].dt.date
        
        # Merge all dataframes
        result = date_range
        
        if daily_mood is not None:
            result = pd.merge(result, daily_mood, on="date", how="left")
        
        if daily_activity is not None:
            result = pd.merge(result, daily_activity, on="date", how="left")
        
        if daily_sleep is not None:
            result = pd.merge(result, daily_sleep, on="date", how="left")
        
        # Convert date to datetime for plotting
        result["date"] = pd.to_datetime(result["date"])
        
        # Add day of week
        result["day_of_week"] = result["date"].dt.dayofweek
        result["day_name"] = result["date"].dt.day_name()
        
        return result
    
    def generate_mood_timeline(self, days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a timeline visualization of mood levels.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No mood data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_timeline.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot mood line
        ax.plot(daily_df["date"], daily_df["mood_mean"], 'o-', color="#3498db", linewidth=2, 
               markersize=6, label="Daily Mood")
        
        # Add range if available
        if "mood_min" in daily_df.columns and "mood_max" in daily_df.columns:
            ax.fill_between(daily_df["date"], daily_df["mood_min"], daily_df["mood_max"], 
                           color="#3498db", alpha=0.2)
        
        # Add trend line
        if len(daily_df) > 5:
            # Get non-NaN mood values
            valid_mood = daily_df[daily_df["mood_mean"].notna()]
            if len(valid_mood) > 5:
                x = np.arange(len(valid_mood))
                y = valid_mood["mood_mean"].values
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                
                trend_x = np.arange(len(valid_mood))
                trend_y = p(trend_x)
                
                # Map trend_x indices back to dates
                trend_dates = valid_mood["date"].values
                
                # Plot trend line
                ax.plot(trend_dates, trend_y, '--', color="#e74c3c", linewidth=2, 
                       label=f"Trend (Slope: {z[0]:.3f})")
        
        # Add average line
        avg_mood = daily_df["mood_mean"].mean()
        ax.axhline(y=avg_mood, color="#2ecc71", linestyle='-', linewidth=1.5, 
                  label=f"Average: {avg_mood:.1f}")
        
        # Format x-axis
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        # Set y-axis limits with some padding
        y_min = max(0, daily_df["mood_mean"].min() - 1)
        y_max = min(11, daily_df["mood_mean"].max() + 1)
        ax.set_ylim(y_min, y_max)
        
        # Add labels and title
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Mood Level", fontsize=12)
        ax.set_title(f"Mood Timeline - Last {days} Days", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add legend
        ax.legend(loc="best", frameon=True, framealpha=0.9)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha="right")
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "mood_timeline.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def generate_mood_by_day_of_week(self, days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of mood by day of week.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No mood data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_by_day.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Aggregate by day of week
        day_of_week_df = daily_df.groupby("day_of_week").agg({
            "mood_mean": ["mean", "std", "count"],
            "day_name": "first"
        }).reset_index()
        
        # Flatten multi-level columns
        day_of_week_df.columns = ["day_of_week", "mood_mean", "mood_std", "count", "day_name"]
        
        # Sort by day of week
        day_of_week_df = day_of_week_df.sort_values("day_of_week")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar colors based on mood level
        colors = [self.mood_cmap((mood - 1) / 9) for mood in day_of_week_df["mood_mean"]]
        
        # Plot bars
        bars = ax.bar(day_of_week_df["day_name"], day_of_week_df["mood_mean"], 
                     yerr=day_of_week_df["mood_std"], capsize=5, color=colors, 
                     edgecolor="gray", alpha=0.8)
        
        # Add count labels
        for i, bar in enumerate(bars):
            count = day_of_week_df.iloc[i]["count"]
            if count > 0:
                ax.text(bar.get_x() + bar.get_width()/2, 0.1, f"n={int(count)}", 
                       ha="center", va="bottom", color="gray", fontsize=9)
        
        # Add average line
        avg_mood = daily_df["mood_mean"].mean()
        ax.axhline(y=avg_mood, color="#e74c3c", linestyle='--', linewidth=1.5, 
                  label=f"Overall Average: {avg_mood:.1f}")
        
        # Set y-axis limits with some padding
        y_min = max(0, day_of_week_df["mood_mean"].min() - day_of_week_df["mood_std"].max() - 0.5)
        y_max = min(11, day_of_week_df["mood_mean"].max() + day_of_week_df["mood_std"].max() + 0.5)
        ax.set_ylim(y_min, y_max)
        
        # Add labels and title
        ax.set_xlabel("Day of Week", fontsize=12)
        ax.set_ylabel("Average Mood Level", fontsize=12)
        ax.set_title(f"Mood by Day of Week - Last {days} Days", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="y")
        
        # Add legend
        ax.legend(loc="best", frameon=True, framealpha=0.9)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "mood_by_day.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def generate_mood_activity_correlation(self, activity_type: Optional[str] = None, 
                                          days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of correlation between mood and activities.
        
        Args:
            activity_type: Optional specific activity to visualize
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No mood data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_activity_correlation.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Find activity columns
        activity_cols = [col for col in daily_df.columns if "_duration" in col]
        
        if not activity_cols:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No activity data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_activity_correlation.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # If specific activity is provided, filter for it
        if activity_type:
            activity_col = f"{activity_type}_duration"
            if activity_col not in activity_cols:
                # Create a simple "no data" visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, f"No data available for activity: {activity_type}", 
                       ha="center", va="center", fontsize=14)
                ax.set_axis_off()
                
                if save_path is None:
                    save_path = os.path.join(self.output_dir, f"mood_activity_{activity_type}.png")
                
                plt.savefig(save_path, bbox_inches="tight", dpi=100)
                plt.close(fig)
                return save_path
            
            activity_cols = [activity_col]
        
        # Create figure
        if len(activity_cols) == 1:
            # Single activity visualization
            activity_col = activity_cols[0]
            activity_name = activity_col.replace("_duration", "")
            
            # Create scatter plot with regression line
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Filter out rows with missing data
            plot_df = daily_df.dropna(subset=["mood_mean", activity_col])
            
            if len(plot_df) < 5:
                ax.text(0.5, 0.5, f"Insufficient data points to visualize correlation", 
                       ha="center", va="center", fontsize=14)
                ax.set_axis_off()
            else:
                # Create scatter plot
                scatter = ax.scatter(plot_df[activity_col], plot_df["mood_mean"], 
                                   c=plot_df["mood_mean"], cmap=self.mood_cmap, 
                                   s=80, alpha=0.7, edgecolor="gray")
                
                # Add regression line
                x = plot_df[activity_col].values
                y = plot_df["mood_mean"].values
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                
                x_range = np.linspace(x.min(), x.max(), 100)
                ax.plot(x_range, p(x_range), '--', color="#e74c3c", linewidth=2)
                
                # Calculate correlation
                corr = plot_df[["mood_mean", activity_col]].corr().iloc[0, 1]
                
                # Add correlation text
                ax.text(0.05, 0.95, f"Correlation: {corr:.2f}", transform=ax.transAxes, 
                       fontsize=12, va="top", ha="left", 
                       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
                # Add labels and title
                ax.set_xlabel(f"{activity_name.title()} Duration (minutes)", fontsize=12)
                ax.set_ylabel("Mood Level", fontsize=12)
                ax.set_title(f"Correlation: Mood vs. {activity_name.title()} - Last {days} Days", 
                            fontsize=14, fontweight="bold")
                
                # Add colorbar
                cbar = plt.colorbar(scatter, ax=ax)
                cbar.set_label("Mood Level")
                
                # Add grid
                ax.grid(True, alpha=0.3)
            
            # Save figure
            if save_path is None:
                save_path = os.path.join(self.output_dir, f"mood_activity_{activity_name}.png")
            
        else:
            # Multiple activities correlation heatmap
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Prepare correlation data
            corr_data = []
            activity_names = []
            
            for col in activity_cols:
                activity_name = col.replace("_duration", "")
                activity_names.append(activity_name)
                
                # Calculate correlation
                corr = daily_df[["mood_mean", col]].corr().iloc[0, 1]
                corr_data.append(corr)
            
            # Sort by correlation strength
            sorted_indices = np.argsort(np.abs(corr_data))[::-1]
            activity_names = [activity_names[i] for i in sorted_indices]
            corr_data = [corr_data[i] for i in sorted_indices]
            
            # Create horizontal bar chart
            bars = ax.barh(activity_names, corr_data, color=[
                self.mood_colors["high"] if c > 0.1 else 
                self.mood_colors["low"] if c < -0.1 else 
                self.mood_colors["medium"] for c in corr_data
            ], alpha=0.7, edgecolor="gray")
            
            # Add correlation values
            for i, bar in enumerate(bars):
                ax.text(
                    bar.get_width() + (0.02 if bar.get_width() >= 0 else -0.08), 
                    bar.get_y() + bar.get_height()/2, 
                    f"{corr_data[i]:.2f}", 
                    va="center", 
                    ha="left" if bar.get_width() >= 0 else "right",
                    fontsize=10
                )
            
            # Add zero line
            ax.axvline(x=0, color="gray", linestyle="-", linewidth=1)
            
            # Set limits
            ax.set_xlim(-1, 1)
            
            # Add labels and title
            ax.set_xlabel("Correlation with Mood", fontsize=12)
            ax.set_ylabel("Activity", fontsize=12)
            ax.set_title(f"Activity-Mood Correlations - Last {days} Days", 
                        fontsize=14, fontweight="bold")
            
            # Add grid
            ax.grid(True, alpha=0.3, axis="x")
            
            # Save figure
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_activity_correlation.png")
        
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def generate_mood_sleep_correlation(self, days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of correlation between mood and sleep.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns or "sleep_duration" not in daily_df.columns:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Insufficient sleep or mood data for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_sleep_correlation.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Filter out rows with missing data
        plot_df = daily_df.dropna(subset=["mood_mean", "sleep_duration"])
        
        if len(plot_df) < 5:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Insufficient data points to visualize sleep-mood correlation", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "mood_sleep_correlation.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot for sleep duration vs mood
        scatter = ax1.scatter(plot_df["sleep_duration"], plot_df["mood_mean"], 
                            c=plot_df["mood_mean"], cmap=self.mood_cmap, 
                            s=80, alpha=0.7, edgecolor="gray")
        
        # Add regression line
        x = plot_df["sleep_duration"].values
        y = plot_df["mood_mean"].values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        x_range = np.linspace(x.min(), x.max(), 100)
        ax1.plot(x_range, p(x_range), '--', color="#e74c3c", linewidth=2)
        
        # Calculate correlation
        duration_corr = plot_df[["mood_mean", "sleep_duration"]].corr().iloc[0, 1]
        
        # Add correlation text
        ax1.text(0.05, 0.95, f"Correlation: {duration_corr:.2f}", transform=ax1.transAxes, 
               fontsize=12, va="top", ha="left", 
               bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        # Add labels and title
        ax1.set_xlabel("Sleep Duration (hours)", fontsize=12)
        ax1.set_ylabel("Mood Level", fontsize=12)
        ax1.set_title("Mood vs. Sleep Duration", fontsize=14, fontweight="bold")
        
        # Add grid
        ax1.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label("Mood Level")
        
        # Second plot: Sleep quality vs mood (if available)
        if "sleep_quality" in plot_df.columns and not plot_df["sleep_quality"].isna().all():
            quality_plot_df = plot_df.dropna(subset=["sleep_quality"])
            
            if len(quality_plot_df) >= 5:
                scatter2 = ax2.scatter(quality_plot_df["sleep_quality"], quality_plot_df["mood_mean"], 
                                     c=quality_plot_df["mood_mean"], cmap=self.mood_cmap, 
                                     s=80, alpha=0.7, edgecolor="gray")
                
                # Add regression line
                x = quality_plot_df["sleep_quality"].values
                y = quality_plot_df["mood_mean"].values
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                
                x_range = np.linspace(x.min(), x.max(), 100)
                ax2.plot(x_range, p(x_range), '--', color="#e74c3c", linewidth=2)
                
                # Calculate correlation
                quality_corr = quality_plot_df[["mood_mean", "sleep_quality"]].corr().iloc[0, 1]
                
                # Add correlation text
                ax2.text(0.05, 0.95, f"Correlation: {quality_corr:.2f}", transform=ax2.transAxes, 
                       fontsize=12, va="top", ha="left", 
                       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
                # Add labels and title
                ax2.set_xlabel("Sleep Quality (1-10)", fontsize=12)
                ax2.set_ylabel("Mood Level", fontsize=12)
                ax2.set_title("Mood vs. Sleep Quality", fontsize=14, fontweight="bold")
                
                # Add grid
                ax2.grid(True, alpha=0.3)
                
                # Add colorbar
                cbar2 = plt.colorbar(scatter2, ax=ax2)
                cbar2.set_label("Mood Level")
            else:
                ax2.text(0.5, 0.5, "Insufficient sleep quality data", 
                       ha="center", va="center", fontsize=14)
                ax2.set_axis_off()
        else:
            ax2.text(0.5, 0.5, "No sleep quality data available", 
                   ha="center", va="center", fontsize=14)
            ax2.set_axis_off()
        
        # Add overall title
        plt.suptitle(f"Sleep-Mood Correlations - Last {days} Days", fontsize=16, fontweight="bold", y=1.05)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "mood_sleep_correlation.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def generate_emotion_distribution(self, days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of emotion distribution.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        # Get mood entries
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        mood_entries = self.data_collector.get_entries_by_date_range(
            "mood_entries", 
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if not mood_entries:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No mood data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "emotion_distribution.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Extract emotions
        all_emotions = []
        for entry in mood_entries:
            if "emotions" in entry and entry["emotions"]:
                all_emotions.extend(entry["emotions"])
        
        if not all_emotions:
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No emotion data available for the selected period", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "emotion_distribution.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Count emotions
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Sort by count
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Limit to top 15 for readability
        if len(sorted_emotions) > 15:
            sorted_emotions = sorted_emotions[:15]
            other_count = sum(count for emotion, count in emotion_counts.items() 
                             if emotion not in [e[0] for e in sorted_emotions])
            if other_count > 0:
                sorted_emotions.append(("Other", other_count))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract data for plotting
        emotions = [e[0] for e in sorted_emotions]
        counts = [e[1] for e in sorted_emotions]
        
        # Define emotion categories and colors
        emotion_categories = {
            "positive": ["happy", "content", "excited", "grateful", "relaxed", "peaceful", 
                        "optimistic", "confident", "inspired", "proud", "energetic", "hopeful"],
            "negative": ["sad", "anxious", "stressed", "angry", "frustrated", "overwhelmed", 
                        "irritated", "disappointed", "worried", "fearful", "tired", "depressed"],
            "neutral": ["calm", "focused", "contemplative", "curious", "surprised", 
                       "nostalgic", "reflective", "alert", "determined"]
        }
        
        category_colors = {
            "positive": "#2ecc71",  # Green
            "negative": "#e74c3c",  # Red
            "neutral": "#3498db",   # Blue
            "other": "#95a5a6"      # Gray
        }
        
        # Assign colors based on emotion categories
        colors = []
        for emotion in emotions:
            if emotion == "Other":
                colors.append(category_colors["other"])
            else:
                emotion_lower = emotion.lower()
                for category, emotion_list in emotion_categories.items():
                    if emotion_lower in emotion_list:
                        colors.append(category_colors[category])
                        break
                else:
                    colors.append(category_colors["other"])
        
        # Create horizontal bar chart
        bars = ax.barh(emotions, counts, color=colors, alpha=0.8, edgecolor="gray")
        
        # Add count labels
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
                   str(counts[i]), va="center", fontsize=10)
        
        # Add labels and title
        ax.set_xlabel("Count", fontsize=12)
        ax.set_ylabel("Emotion", fontsize=12)
        ax.set_title(f"Emotion Distribution - Last {days} Days", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="x")
        
        # Add legend for categories
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color=category_colors["positive"], alpha=0.8, edgecolor="gray", label="Positive"),
            plt.Rectangle((0, 0), 1, 1, color=category_colors["negative"], alpha=0.8, edgecolor="gray", label="Negative"),
            plt.Rectangle((0, 0), 1, 1, color=category_colors["neutral"], alpha=0.8, edgecolor="gray", label="Neutral"),
            plt.Rectangle((0, 0), 1, 1, color=category_colors["other"], alpha=0.8, edgecolor="gray", label="Other")
        ]
        ax.legend(handles=legend_elements, loc="lower right")
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "emotion_distribution.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def generate_pattern_visualization(self, pattern_data: Dict[str, Any], 
                                      days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of identified patterns.
        
        Args:
            pattern_data: Pattern data from pattern recognition engine
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        if pattern_data.get("status") != "success":
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Insufficient data to identify patterns", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "pattern_visualization.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(15, 12))
        
        # Define grid layout
        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
        
        # Time of day patterns
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_time_of_day_patterns(ax1, pattern_data)
        
        # Day of week patterns
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_day_of_week_patterns(ax2, pattern_data)
        
        # Trend analysis
        ax3 = fig.add_subplot(gs[1, :])
        self._plot_trend_analysis(ax3, days)
        
        # Insights
        ax4 = fig.add_subplot(gs[2, :])
        self._plot_insights(ax4, pattern_data)
        
        # Add overall title
        plt.suptitle(f"Mood Patterns - Last {days} Days", fontsize=16, fontweight="bold", y=0.98)
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "pattern_visualization.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def _plot_time_of_day_patterns(self, ax, pattern_data):
        """Helper to plot time of day patterns."""
        time_data = pattern_data.get("time_of_day", {})
        
        times = ["morning", "afternoon", "evening"]
        values = [time_data.get(t) for t in times]
        
        # Check if we have valid data
        if all(v is None for v in values):
            ax.text(0.5, 0.5, "No time of day pattern data available", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Replace None with 0
        values = [v if v is not None else 0 for v in values]
        
        # Create bar colors based on mood level
        colors = [self.mood_cmap((v - 1) / 9) if v > 0 else "#95a5a6" for v in values]
        
        # Plot bars
        bars = ax.bar(times, values, color=colors, alpha=0.8, edgecolor="gray")
        
        # Add value labels
        for i, bar in enumerate(bars):
            if values[i] > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                       f"{values[i]:.1f}", ha="center", va="bottom", fontsize=10)
        
        # Add best time indicator if available
        best_time = time_data.get("best_time")
        if best_time:
            best_index = times.index(best_time)
            ax.text(bars[best_index].get_x() + bars[best_index].get_width()/2, 
                   values[best_index] / 2, "★", ha="center", va="center", 
                   fontsize=20, color="white")
        
        # Add labels and title
        ax.set_xlabel("Time of Day", fontsize=12)
        ax.set_ylabel("Average Mood Level", fontsize=12)
        ax.set_title("Mood by Time of Day", fontsize=14, fontweight="bold")
        
        # Set y-axis limits with some padding
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 10)
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="y")
    
    def _plot_day_of_week_patterns(self, ax, pattern_data):
        """Helper to plot day of week patterns."""
        day_data = pattern_data.get("day_of_week", {})
        
        # Check if we have valid data
        if day_data.get("weekday") is None and day_data.get("weekend") is None:
            ax.text(0.5, 0.5, "No day of week pattern data available", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Get values
        weekday = day_data.get("weekday", 0)
        weekend = day_data.get("weekend", 0)
        
        # Create bar colors based on mood level
        colors = [
            self.mood_cmap((weekday - 1) / 9) if weekday > 0 else "#95a5a6",
            self.mood_cmap((weekend - 1) / 9) if weekend > 0 else "#95a5a6"
        ]
        
        # Plot bars
        bars = ax.bar(["Weekdays", "Weekends"], [weekday, weekend], color=colors, 
                     alpha=0.8, edgecolor="gray")
        
        # Add value labels
        for i, bar in enumerate(bars):
            if [weekday, weekend][i] > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                       f"{[weekday, weekend][i]:.1f}", ha="center", va="bottom", fontsize=10)
        
        # Add better period indicator if available
        better_period = day_data.get("better_period")
        if better_period == "weekdays":
            ax.text(bars[0].get_x() + bars[0].get_width()/2, 
                   weekday / 2, "★", ha="center", va="center", 
                   fontsize=20, color="white")
        elif better_period == "weekends":
            ax.text(bars[1].get_x() + bars[1].get_width()/2, 
                   weekend / 2, "★", ha="center", va="center", 
                   fontsize=20, color="white")
        
        # Add labels and title
        ax.set_xlabel("Period", fontsize=12)
        ax.set_ylabel("Average Mood Level", fontsize=12)
        ax.set_title("Mood: Weekdays vs. Weekends", fontsize=14, fontweight="bold")
        
        # Set y-axis limits with some padding
        ax.set_ylim(0, max(weekday, weekend) * 1.2 if max(weekday, weekend) > 0 else 10)
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="y")
    
    def _plot_trend_analysis(self, ax, days):
        """Helper to plot trend analysis."""
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns or len(daily_df) < 7:
            ax.text(0.5, 0.5, "Insufficient data for trend analysis", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Plot mood line
        ax.plot(daily_df["date"], daily_df["mood_mean"], 'o-', color="#3498db", 
               linewidth=2, markersize=4, alpha=0.7, label="Daily Mood")
        
        # Add trend line
        valid_mood = daily_df[daily_df["mood_mean"].notna()]
        if len(valid_mood) > 5:
            x = np.arange(len(valid_mood))
            y = valid_mood["mood_mean"].values
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            
            trend_x = np.arange(len(valid_mood))
            trend_y = p(trend_x)
            
            # Map trend_x indices back to dates
            trend_dates = valid_mood["date"].values
            
            # Plot trend line
            ax.plot(trend_dates, trend_y, '-', color="#e74c3c", linewidth=3, 
                   label=f"Trend (Slope: {z[0]:.3f})")
            
            # Add trend direction text
            if z[0] > 0.05:
                trend_text = "Improving Trend"
                trend_color = "#2ecc71"
            elif z[0] < -0.05:
                trend_text = "Declining Trend"
                trend_color = "#e74c3c"
            else:
                trend_text = "Stable Trend"
                trend_color = "#3498db"
            
            ax.text(0.02, 0.95, trend_text, transform=ax.transAxes, 
                   fontsize=14, fontweight="bold", va="top", ha="left", 
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=trend_color, alpha=0.8),
                   color=trend_color)
        
        # Add 7-day moving average
        if len(daily_df) >= 7:
            daily_df["mood_7day_avg"] = daily_df["mood_mean"].rolling(window=7, min_periods=1).mean()
            ax.plot(daily_df["date"], daily_df["mood_7day_avg"], '-', color="#2ecc71", 
                   linewidth=2, label="7-Day Average")
        
        # Format x-axis
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        # Add labels and title
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Mood Level", fontsize=12)
        ax.set_title("Mood Trend Analysis", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add legend
        ax.legend(loc="upper right", frameon=True, framealpha=0.9)
        
        # Rotate x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    
    def _plot_insights(self, ax, pattern_data):
        """Helper to plot insights."""
        insights = pattern_data.get("insights", [])
        
        if not insights:
            ax.text(0.5, 0.5, "No insights available", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Remove axis
        ax.set_axis_off()
        
        # Add title
        ax.text(0.5, 1.0, "Key Insights", fontsize=14, fontweight="bold", 
               ha="center", va="top", transform=ax.transAxes)
        
        # Add insights as bullet points
        y_pos = 0.9
        for i, insight in enumerate(insights):
            ax.text(0.1, y_pos, f"• {insight}", fontsize=12, 
                   ha="left", va="top", transform=ax.transAxes,
                   wrap=True)
            y_pos -= 0.15
            
            # Limit to 5 insights to avoid overcrowding
            if i >= 4:
                if len(insights) > 5:
                    ax.text(0.1, y_pos, f"• Plus {len(insights) - 5} more insights...", 
                           fontsize=12, ha="left", va="top", transform=ax.transAxes,
                           color="gray", style="italic")
                break
    
    def generate_correlation_visualization(self, correlation_data: Dict[str, Any], 
                                          days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a visualization of correlation analysis results.
        
        Args:
            correlation_data: Correlation data from correlation analyzer
            days: Number of days to include
            save_path: Optional path to save the visualization
            
        Returns:
            Path to saved visualization
        """
        # Check if we have valid data
        if not correlation_data or all(corr.get("status") != "success" for corr in correlation_data.values() 
                                     if isinstance(corr, dict)):
            # Create a simple "no data" visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Insufficient data for correlation analysis", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            
            if save_path is None:
                save_path = os.path.join(self.output_dir, "correlation_visualization.png")
            
            plt.savefig(save_path, bbox_inches="tight", dpi=100)
            plt.close(fig)
            return save_path
        
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(15, 12))
        
        # Define grid layout
        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
        
        # Lagged correlations
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_lagged_correlations(ax1, correlation_data.get("lagged_correlations", {}))
        
        # Granger causality
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_granger_causality(ax2, correlation_data.get("granger_causality", {}))
        
        # Mood cycles
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_mood_cycles(ax3, correlation_data.get("mood_cycles", {}))
        
        # Multivariate relationships
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_multivariate_relationships(ax4, correlation_data.get("multivariate_relationships", {}))
        
        # Key insights
        ax5 = fig.add_subplot(gs[2, :])
        self._plot_correlation_insights(ax5, correlation_data.get("key_insights", []))
        
        # Add overall title
        plt.suptitle(f"Correlation Analysis - Last {days} Days", fontsize=16, fontweight="bold", y=0.98)
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, "correlation_visualization.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def _plot_lagged_correlations(self, ax, lagged_data):
        """Helper to plot lagged correlations."""
        if lagged_data.get("status") != "success" or not lagged_data.get("lag_results"):
            ax.text(0.5, 0.5, "No significant lagged correlations found", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Get top 5 results
        results = lagged_data.get("lag_results", [])[:5]
        
        # Prepare data for plotting
        variables = []
        correlations = []
        lags = []
        
        for result in results:
            var_name = result["variable"].replace("_", " ").title()
            strongest = result["strongest_lag"]
            
            variables.append(var_name)
            correlations.append(strongest["correlation"])
            lags.append(strongest["lag"])
        
        # Create horizontal bar chart
        y_pos = np.arange(len(variables))
        bars = ax.barh(y_pos, correlations, color=[
            self.mood_colors["high"] if c > 0.1 else 
            self.mood_colors["low"] if c < -0.1 else 
            self.mood_colors["medium"] for c in correlations
        ], alpha=0.7, edgecolor="gray")
        
        # Add variable names and lag information
        for i, (var, lag) in enumerate(zip(variables, lags)):
            ax.text(-0.01, i, f"{var} (Lag {lag})", ha="right", va="center", fontsize=10)
        
        # Add correlation values
        for i, bar in enumerate(bars):
            ax.text(
                bar.get_width() + (0.02 if bar.get_width() >= 0 else -0.08), 
                bar.get_y() + bar.get_height()/2, 
                f"{correlations[i]:.2f}", 
                va="center", 
                ha="left" if bar.get_width() >= 0 else "right",
                fontsize=10
            )
        
        # Add zero line
        ax.axvline(x=0, color="gray", linestyle="-", linewidth=1)
        
        # Set limits
        ax.set_xlim(-1, 1)
        
        # Remove y-axis labels
        ax.set_yticks([])
        
        # Add labels and title
        ax.set_xlabel("Correlation Strength", fontsize=12)
        ax.set_title("Lagged Correlations with Mood", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="x")
    
    def _plot_granger_causality(self, ax, causality_data):
        """Helper to plot Granger causality results."""
        if causality_data.get("status") != "success" or not causality_data.get("causality_results"):
            ax.text(0.5, 0.5, "No significant causal relationships found", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Get results
        results = causality_data.get("causality_results", [])
        
        # Filter to include only the most significant result for each variable
        filtered_results = {}
        for result in results:
            var = result["variable"]
            if var not in filtered_results or result["most_significant_lag"]["p_value"] < filtered_results[var]["most_significant_lag"]["p_value"]:
                filtered_results[var] = result
        
        # Get top 5 results
        top_results = sorted(filtered_results.values(), key=lambda x: x["most_significant_lag"]["p_value"])[:5]
        
        # Prepare data for plotting
        relationships = []
        p_values = []
        lags = []
        
        for result in top_results:
            var_name = result["variable"].replace("_", " ").title()
            direction = result["direction"]
            lag = result["most_significant_lag"]["lag"]
            p_value = result["most_significant_lag"]["p_value"]
            
            if "→ mood" in direction:
                relationships.append(f"{var_name} → Mood")
            else:
                relationships.append(f"Mood → {var_name}")
            
            p_values.append(p_value)
            lags.append(lag)
        
        # Create horizontal bar chart for -log(p-value)
        y_pos = np.arange(len(relationships))
        log_p_values = [-np.log10(p) for p in p_values]
        
        bars = ax.barh(y_pos, log_p_values, color="#3498db", alpha=0.7, edgecolor="gray")
        
        # Add relationship and lag information
        for i, (rel, lag) in enumerate(zip(relationships, lags)):
            ax.text(-0.01, i, f"{rel} (Lag {lag})", ha="right", va="center", fontsize=10)
        
        # Add p-value information
        for i, (bar, p) in enumerate(zip(bars, p_values)):
            ax.text(
                bar.get_width() + 0.1, 
                bar.get_y() + bar.get_height()/2, 
                f"p={p:.4f}", 
                va="center", 
                ha="left",
                fontsize=10
            )
        
        # Add significance threshold line
        threshold = -np.log10(0.05)
        ax.axvline(x=threshold, color="#e74c3c", linestyle="--", linewidth=1.5, 
                  label="p=0.05 threshold")
        
        # Remove y-axis labels
        ax.set_yticks([])
        
        # Add labels and title
        ax.set_xlabel("-log10(p-value)", fontsize=12)
        ax.set_title("Granger Causality Tests", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="x")
        
        # Add legend
        ax.legend(loc="lower right")
    
    def _plot_mood_cycles(self, ax, cycle_data):
        """Helper to plot mood cycles."""
        if cycle_data.get("status") != "success" or not cycle_data.get("cycles"):
            ax.text(0.5, 0.5, "No significant mood cycles detected", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Get cycle data
        cycles = cycle_data.get("cycles", [])
        
        # Prepare data for plotting
        cycle_lengths = [c["length"] for c in cycles]
        cycle_strengths = [c["strength"] for c in cycles]
        cycle_types = [c["type"] for c in cycles]
        
        # Create bar chart
        bars = ax.bar(cycle_lengths, cycle_strengths, color=[
            "#e74c3c" if t == "primary" else
            "#3498db" if t == "weekly" else
            "#2ecc71" for t in cycle_types
        ], alpha=0.7, edgecolor="gray")
        
        # Add strength labels
        for i, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                   f"{cycle_strengths[i]:.2f}", ha="center", va="bottom", fontsize=10)
        
        # Add significance threshold
        ax.axhline(y=0.2, color="gray", linestyle="--", linewidth=1, 
                  label="Significance Threshold")
        
        # Add labels and title
        ax.set_xlabel("Cycle Length (days)", fontsize=12)
        ax.set_ylabel("Strength (Autocorrelation)", fontsize=12)
        ax.set_title("Mood Cycles", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="y")
        
        # Add legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color="#e74c3c", alpha=0.7, edgecolor="gray", label="Primary"),
            plt.Rectangle((0, 0), 1, 1, color="#3498db", alpha=0.7, edgecolor="gray", label="Weekly"),
            plt.Rectangle((0, 0), 1, 1, color="#2ecc71", alpha=0.7, edgecolor="gray", label="Secondary")
        ]
        ax.legend(handles=legend_elements, loc="upper right")
    
    def _plot_multivariate_relationships(self, ax, multivariate_data):
        """Helper to plot multivariate relationships."""
        if multivariate_data.get("status") != "success":
            ax.text(0.5, 0.5, "Insufficient data for multivariate analysis", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Check if we have PCA results
        pca_results = multivariate_data.get("pca_analysis", {})
        if "mood_related_variables" not in pca_results or not pca_results["mood_related_variables"]:
            ax.text(0.5, 0.5, "No significant multivariate relationships found", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Get related variables
        related_vars = pca_results["mood_related_variables"]
        
        # Prepare data for plotting
        variables = []
        loadings = []
        relationships = []
        
        for var in related_vars:
            var_name = var["variable"].replace("_", " ").title()
            loading = var["loading"]
            relationship = var["relationship"]
            
            variables.append(var_name)
            loadings.append(loading)
            relationships.append(relationship)
        
        # Create horizontal bar chart
        y_pos = np.arange(len(variables))
        bars = ax.barh(y_pos, loadings, color=[
            self.mood_colors["high"] if r == "positive" else self.mood_colors["low"]
            for r in relationships
        ], alpha=0.7, edgecolor="gray")
        
        # Add variable names
        for i, var in enumerate(variables):
            ax.text(-0.01, i, var, ha="right", va="center", fontsize=10)
        
        # Add loading values
        for i, bar in enumerate(bars):
            ax.text(
                bar.get_width() + (0.02 if bar.get_width() >= 0 else -0.08), 
                bar.get_y() + bar.get_height()/2, 
                f"{loadings[i]:.2f}", 
                va="center", 
                ha="left" if bar.get_width() >= 0 else "right",
                fontsize=10
            )
        
        # Add zero line
        ax.axvline(x=0, color="gray", linestyle="-", linewidth=1)
        
        # Set limits
        ax.set_xlim(-1, 1)
        
        # Remove y-axis labels
        ax.set_yticks([])
        
        # Add labels and title
        ax.set_xlabel("Component Loading", fontsize=12)
        ax.set_title("Multivariate Relationships (PCA)", fontsize=14, fontweight="bold")
        
        # Add grid
        ax.grid(True, alpha=0.3, axis="x")
        
        # Add legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, color=self.mood_colors["high"], alpha=0.7, 
                         edgecolor="gray", label="Positive Relationship"),
            plt.Rectangle((0, 0), 1, 1, color=self.mood_colors["low"], alpha=0.7, 
                         edgecolor="gray", label="Negative Relationship")
        ]
        ax.legend(handles=legend_elements, loc="lower right")
    
    def _plot_correlation_insights(self, ax, insights):
        """Helper to plot correlation insights."""
        if not insights:
            ax.text(0.5, 0.5, "No significant insights found", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
            return
        
        # Remove axis
        ax.set_axis_off()
        
        # Add title
        ax.text(0.5, 1.0, "Key Correlation Insights", fontsize=14, fontweight="bold", 
               ha="center", va="top", transform=ax.transAxes)
        
        # Add insights as bullet points
        y_pos = 0.9
        for i, insight in enumerate(insights):
            ax.text(0.1, y_pos, f"• {insight}", fontsize=12, 
                   ha="left", va="top", transform=ax.transAxes,
                   wrap=True)
            y_pos -= 0.15
            
            # Limit to 5 insights to avoid overcrowding
            if i >= 4:
                if len(insights) > 5:
                    ax.text(0.1, y_pos, f"• Plus {len(insights) - 5} more insights...", 
                           fontsize=12, ha="left", va="top", transform=ax.transAxes,
                           color="gray", style="italic")
                break
    
    def generate_dashboard(self, days: int = 90, save_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive dashboard with multiple visualizations.
        
        Args:
            days: Number of days to include
            save_path: Optional path to save the dashboard
            
        Returns:
            Path to saved dashboard
        """
        # Create individual visualizations
        mood_timeline_path = self.generate_mood_timeline(days)
        mood_by_day_path = self.generate_mood_by_day_of_week(days)
        emotion_distribution_path = self.generate_emotion_distribution(days)
        mood_activity_path = self.generate_mood_activity_correlation(days=days)
        mood_sleep_path = self.generate_mood_sleep_correlation(days)
        
        # Create dashboard figure
        fig = plt.figure(figsize=(20, 24))
        
        # Define grid layout
        gs = fig.add_gridspec(5, 2, hspace=0.4, wspace=0.3, height_ratios=[1, 1, 1, 1, 0.5])
        
        # Add title
        fig.suptitle(f"Mental Health Dashboard - Last {days} Days", fontsize=24, fontweight="bold", y=0.98)
        
        # Add visualizations
        self._add_image_to_subplot(fig, gs[0, :], mood_timeline_path, "Mood Timeline")
        self._add_image_to_subplot(fig, gs[1, 0], mood_by_day_path, "Mood by Day of Week")
        self._add_image_to_subplot(fig, gs[1, 1], emotion_distribution_path, "Emotion Distribution")
        self._add_image_to_subplot(fig, gs[2, :], mood_activity_path, "Activity-Mood Correlations")
        self._add_image_to_subplot(fig, gs[3, :], mood_sleep_path, "Sleep-Mood Correlations")
        
        # Add summary and insights
        ax_summary = fig.add_subplot(gs[4, :])
        self._add_dashboard_summary(ax_summary, days)
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save dashboard
        if save_path is None:
            save_path = os.path.join(self.output_dir, "dashboard.png")
        
        plt.savefig(save_path, bbox_inches="tight", dpi=100)
        plt.close(fig)
        
        return save_path
    
    def _add_image_to_subplot(self, fig, gridspec, image_path, title):
        """Helper to add an image to a subplot."""
        ax = fig.add_subplot(gridspec)
        
        try:
            img = plt.imread(image_path)
            ax.imshow(img)
            ax.set_title(title, fontsize=16, fontweight="bold")
            ax.set_axis_off()
        except Exception as e:
            ax.text(0.5, 0.5, f"Error loading visualization: {str(e)}", 
                   ha="center", va="center", fontsize=12)
            ax.set_axis_off()
    
    def _add_dashboard_summary(self, ax, days):
        """Helper to add summary and insights to dashboard."""
        # Get data for summary
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns:
            ax.text(0.5, 0.5, "Insufficient data for summary", 
                   ha="center", va="center", fontsize=14)
            ax.set_axis_off()
            return
        
        # Calculate summary statistics
        avg_mood = daily_df["mood_mean"].mean()
        mood_range = (daily_df["mood_mean"].min(), daily_df["mood_mean"].max())
        
        # Calculate trend
        if len(daily_df) > 5:
            valid_mood = daily_df[daily_df["mood_mean"].notna()]
            if len(valid_mood) > 5:
                x = np.arange(len(valid_mood))
                y = valid_mood["mood_mean"].values
                z = np.polyfit(x, y, 1)
                trend = z[0]
                
                if trend > 0.05:
                    trend_text = "Improving"
                    trend_color = "#2ecc71"
                elif trend < -0.05:
                    trend_text = "Declining"
                    trend_color = "#e74c3c"
                else:
                    trend_text = "Stable"
                    trend_color = "#3498db"
            else:
                trend_text = "Unknown"
                trend_color = "gray"
        else:
            trend_text = "Unknown"
            trend_color = "gray"
        
        # Remove axis
        ax.set_axis_off()
        
        # Add title
        ax.text(0.5, 1.0, "Dashboard Summary", fontsize=16, fontweight="bold", 
               ha="center", va="top", transform=ax.transAxes)
        
        # Add summary statistics
        ax.text(0.1, 0.8, f"Average Mood: {avg_mood:.1f}/10", fontsize=14, 
               ha="left", va="top", transform=ax.transAxes)
        
        ax.text(0.1, 0.6, f"Mood Range: {mood_range[0]:.1f} - {mood_range[1]:.1f}", 
               fontsize=14, ha="left", va="top", transform=ax.transAxes)
        
        ax.text(0.1, 0.4, f"Overall Trend: ", fontsize=14, 
               ha="left", va="top", transform=ax.transAxes)
        
        ax.text(0.3, 0.4, trend_text, fontsize=14, fontweight="bold", 
               ha="left", va="top", transform=ax.transAxes, color=trend_color)
        
        # Add data coverage information
        data_days = len(daily_df[daily_df["mood_mean"].notna()])
        coverage = (data_days / len(daily_df)) * 100
        
        ax.text(0.6, 0.8, f"Data Coverage: {data_days}/{len(daily_df)} days ({coverage:.1f}%)", 
               fontsize=14, ha="left", va="top", transform=ax.transAxes)
        
        # Add date range
        start_date = daily_df["date"].min().strftime("%b %d, %Y")
        end_date = daily_df["date"].max().strftime("%b %d, %Y")
        
        ax.text(0.6, 0.6, f"Date Range: {start_date} - {end_date}", 
               fontsize=14, ha="left", va="top", transform=ax.transAxes)


# Example usage
if __name__ == "__main__":
    from src.data_collection import DataCollector
    from src.pattern_recognition import PatternRecognitionEngine
    from src.correlation_analysis import CorrelationAnalyzer
    import matplotlib.pyplot as plt
    
    # Create data collector and add sample data
    collector = DataCollector()
    
    # Add some sample data spanning multiple days with patterns
    for i in range(60):
        # Create a date i days ago
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        
        # Create weekly cycle in mood (better on weekends)
        is_weekend = date.weekday() >= 5
        base_mood = 7 if is_weekend else 5
        
        # Add some random variation
        mood = max(1, min(10, base_mood + np.random.randint(-1, 2)))
        
        # Record mood
        collector.record_mood(
            mood_level=mood,
            notes="Daily entry",
            emotions=["happy" if mood > 6 else "neutral" if mood > 4 else "sad"],
            timestamp=date.replace(hour=12).isoformat()
        )
        
        # Add exercise every 3 days, which improves mood the next day
        if i % 3 == 0:
            collector.record_activity(
                activity_type="exercise",
                duration_minutes=30,
                intensity=4,
                notes="Workout",
                timestamp=date.replace(hour=18).isoformat()
            )
            
            # Mood is better the day after exercise
            if i > 0:
                next_day = date + datetime.timedelta(days=1)
                next_day_mood = min(10, mood + 2)
                
                collector.record_mood(
                    mood_level=next_day_mood,
                    notes="Day after exercise",
                    emotions=["energetic", "positive"],
                    timestamp=next_day.replace(hour=12).isoformat()
                )
        
        # Add sleep entries with a pattern (better sleep on weekends)
        sleep_duration = 8 if is_weekend else 6.5
        collector.record_sleep(
            duration_hours=sleep_duration,
            quality=7 if sleep_duration >= 7.5 else 5,
            notes="Sleep record",
            start_time=date.replace(hour=23).isoformat(),
            end_time=date.replace(hour=7).isoformat()
        )
    
    # Create visualization generator
    viz_generator = VisualizationGenerator(collector)
    
    # Generate visualizations
    mood_timeline = viz_generator.generate_mood_timeline()
    print(f"Generated mood timeline: {mood_timeline}")
    
    mood_by_day = viz_generator.generate_mood_by_day_of_week()
    print(f"Generated mood by day: {mood_by_day}")
    
    mood_activity = viz_generator.generate_mood_activity_correlation()
    print(f"Generated mood-activity correlation: {mood_activity}")
    
    mood_sleep = viz_generator.generate_mood_sleep_correlation()
    print(f"Generated mood-sleep correlation: {mood_sleep}")
    
    emotion_dist = viz_generator.generate_emotion_distribution()
    print(f"Generated emotion distribution: {emotion_dist}")
    
    # Generate pattern visualization
    pattern_engine = PatternRecognitionEngine(collector)
    patterns = pattern_engine.identify_mood_patterns()
    
    pattern_viz = viz_generator.generate_pattern_visualization(patterns)
    print(f"Generated pattern visualization: {pattern_viz}")
    
    # Generate correlation visualization
    corr_analyzer = CorrelationAnalyzer(collector)
    correlations = corr_analyzer.generate_comprehensive_correlation_analysis()
    
    corr_viz = viz_generator.generate_correlation_visualization(correlations)
    print(f"Generated correlation visualization: {corr_viz}")
    
    # Generate dashboard
    dashboard = viz_generator.generate_dashboard()
    print(f"Generated dashboard: {dashboard}")
