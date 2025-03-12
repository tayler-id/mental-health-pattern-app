"""
Correlation Analysis Module for Mental Health Pattern Recognition Assistant

This module provides advanced correlation analysis algorithms to identify relationships
between different aspects of mental health data, including lagged effects,
multivariate analysis, and causality testing.
"""

import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from scipy.stats import pearsonr, spearmanr
from statsmodels.tsa.stattools import grangercausalitytests, acf, pacf
from statsmodels.tsa.api import VAR
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.data_collection import DataCollector

class CorrelationAnalyzer:
    """
    Provides advanced correlation analysis for mental health data.
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize the correlation analyzer with a data collector.
        
        Args:
            data_collector: Optional DataCollector instance, creates a new one if None
        """
        self.data_collector = data_collector or DataCollector()
    
    def _prepare_daily_dataframe(self, days: int = 90) -> pd.DataFrame:
        """
        Prepare a daily aggregated DataFrame from collected data for analysis.
        
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
            daily_mood = mood_df.groupby("date")["mood_level"].agg(['mean', 'min', 'max', 'std']).reset_index()
            daily_mood.columns = ["date", "mood_mean", "mood_min", "mood_max", "mood_std"]
            # Replace NaN with 0 for std
            daily_mood["mood_std"] = daily_mood["mood_std"].fillna(0)
        
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
            # Replace NaN with mean for quality
            if "sleep_quality" in daily_sleep.columns:
                mean_quality = daily_sleep["sleep_quality"].mean()
                daily_sleep["sleep_quality"] = daily_sleep["sleep_quality"].fillna(mean_quality)
        
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
        
        # Fill missing values
        if "mood_mean" in result.columns:
            # Forward fill mood data (use previous day's mood if missing)
            result["mood_mean"] = result["mood_mean"].fillna(method="ffill")
            # Then backward fill (for the first days if missing)
            result["mood_mean"] = result["mood_mean"].fillna(method="bfill")
            # If still missing, use the mean
            result["mood_mean"] = result["mood_mean"].fillna(result["mood_mean"].mean())
            
            # Do the same for other mood columns
            for col in ["mood_min", "mood_max", "mood_std"]:
                if col in result.columns:
                    result[col] = result[col].fillna(method="ffill").fillna(method="bfill").fillna(0)
        
        # Fill missing activity data with 0 (no activity)
        for col in result.columns:
            if "_duration" in col:
                result[col] = result[col].fillna(0)
            elif "_intensity" in col:
                result[col] = result[col].fillna(0)
        
        # Fill missing sleep data
        if "sleep_duration" in result.columns:
            # Forward fill sleep data
            result["sleep_duration"] = result["sleep_duration"].fillna(method="ffill")
            # Then backward fill
            result["sleep_duration"] = result["sleep_duration"].fillna(method="bfill")
            # If still missing, use the mean
            result["sleep_duration"] = result["sleep_duration"].fillna(result["sleep_duration"].mean())
            
            # Do the same for sleep quality
            if "sleep_quality" in result.columns:
                result["sleep_quality"] = result["sleep_quality"].fillna(method="ffill").fillna(method="bfill")
                result["sleep_quality"] = result["sleep_quality"].fillna(result["sleep_quality"].mean())
        
        return result
    
    def analyze_lagged_correlations(self, days: int = 90, max_lag: int = 7) -> Dict[str, Any]:
        """
        Analyze lagged correlations between activities/sleep and mood.
        
        Args:
            days: Number of days of data to analyze
            max_lag: Maximum number of days to lag
            
        Returns:
            Dictionary with lagged correlation results and insights
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns:
            return {
                "status": "insufficient_data",
                "message": "No mood data available for analysis"
            }
        
        # Identify potential predictor columns
        predictor_cols = []
        for col in daily_df.columns:
            if col != "date" and "mood_" not in col:
                predictor_cols.append(col)
        
        if not predictor_cols:
            return {
                "status": "insufficient_data",
                "message": "No predictor variables (activities, sleep) available for analysis"
            }
        
        # Calculate lagged correlations
        lag_results = []
        
        for col in predictor_cols:
            # Skip columns with all zeros or NaN
            if daily_df[col].sum() == 0 or daily_df[col].isna().all():
                continue
                
            lag_correlations = []
            
            # Calculate correlation at different lags
            for lag in range(max_lag + 1):
                # Create lagged variable
                lagged_col = f"{col}_lag{lag}"
                daily_df[lagged_col] = daily_df[col].shift(lag)
                
                # Calculate correlation with mood
                if lag > 0:  # Only include in results if it's actually lagged
                    corr, p = pearsonr(daily_df["mood_mean"].iloc[lag:], daily_df[lagged_col].iloc[lag:])
                    
                    lag_correlations.append({
                        "lag": lag,
                        "correlation": float(corr),
                        "p_value": float(p),
                        "significant": p < 0.05
                    })
            
            # Find the lag with the strongest correlation
            if lag_correlations:
                strongest_lag = max(lag_correlations, key=lambda x: abs(x["correlation"]))
                
                # Only include if there's a meaningful correlation
                if abs(strongest_lag["correlation"]) > 0.2:
                    lag_results.append({
                        "variable": col,
                        "lag_correlations": lag_correlations,
                        "strongest_lag": strongest_lag
                    })
        
        # Sort by strength of correlation
        lag_results.sort(key=lambda x: abs(x["strongest_lag"]["correlation"]), reverse=True)
        
        # Generate insights
        insights = []
        
        for result in lag_results:
            if result["strongest_lag"]["significant"]:
                var_name = result["variable"].replace("_", " ")
                lag = result["strongest_lag"]["lag"]
                corr = result["strongest_lag"]["correlation"]
                
                if corr > 0.3:
                    insights.append(f"{var_name.title()} appears to positively affect your mood {lag} day{'s' if lag > 1 else ''} later.")
                elif corr < -0.3:
                    insights.append(f"{var_name.title()} appears to negatively affect your mood {lag} day{'s' if lag > 1 else ''} later.")
        
        return {
            "status": "success",
            "lag_results": lag_results,
            "insights": insights
        }
    
    def analyze_granger_causality(self, days: int = 90, max_lag: int = 7) -> Dict[str, Any]:
        """
        Perform Granger causality tests to identify potential causal relationships.
        
        Args:
            days: Number of days of data to analyze
            max_lag: Maximum number of days to lag
            
        Returns:
            Dictionary with Granger causality results and insights
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns or len(daily_df) < max_lag + 10:
            return {
                "status": "insufficient_data",
                "message": f"Need at least {max_lag + 10} days of data for Granger causality testing"
            }
        
        # Identify potential predictor columns
        predictor_cols = []
        for col in daily_df.columns:
            if col != "date" and "mood_" not in col:
                # Skip columns with all zeros or NaN
                if daily_df[col].sum() == 0 or daily_df[col].isna().all():
                    continue
                predictor_cols.append(col)
        
        if not predictor_cols:
            return {
                "status": "insufficient_data",
                "message": "No predictor variables (activities, sleep) available for analysis"
            }
        
        # Perform Granger causality tests
        causality_results = []
        
        for col in predictor_cols:
            # Prepare data for testing
            test_df = daily_df[["mood_mean", col]].dropna()
            
            if len(test_df) < max_lag + 10:
                continue
                
            # Run Granger causality test
            try:
                # Test if predictor Granger-causes mood
                predictor_to_mood = grangercausalitytests(
                    test_df[["mood_mean", col]], 
                    maxlag=max_lag,
                    verbose=False
                )
                
                # Extract p-values for each lag
                p_values = []
                for lag in range(1, max_lag + 1):
                    # Use F-test p-value
                    p_value = predictor_to_mood[lag][0]["ssr_ftest"][1]
                    p_values.append({
                        "lag": lag,
                        "p_value": float(p_value),
                        "significant": p_value < 0.05
                    })
                
                # Find the most significant lag
                significant_lags = [lag for lag in p_values if lag["significant"]]
                
                if significant_lags:
                    min_p_lag = min(significant_lags, key=lambda x: x["p_value"])
                    
                    causality_results.append({
                        "variable": col,
                        "direction": f"{col} → mood",
                        "p_values": p_values,
                        "most_significant_lag": min_p_lag,
                        "has_causality": True
                    })
                else:
                    causality_results.append({
                        "variable": col,
                        "direction": f"{col} → mood",
                        "p_values": p_values,
                        "has_causality": False
                    })
                    
                # Test reverse causality (mood Granger-causes predictor)
                mood_to_predictor = grangercausalitytests(
                    test_df[[col, "mood_mean"]], 
                    maxlag=max_lag,
                    verbose=False
                )
                
                # Extract p-values for each lag
                reverse_p_values = []
                for lag in range(1, max_lag + 1):
                    # Use F-test p-value
                    p_value = mood_to_predictor[lag][0]["ssr_ftest"][1]
                    reverse_p_values.append({
                        "lag": lag,
                        "p_value": float(p_value),
                        "significant": p_value < 0.05
                    })
                
                # Find the most significant lag
                reverse_significant_lags = [lag for lag in reverse_p_values if lag["significant"]]
                
                if reverse_significant_lags:
                    reverse_min_p_lag = min(reverse_significant_lags, key=lambda x: x["p_value"])
                    
                    causality_results.append({
                        "variable": col,
                        "direction": f"mood → {col}",
                        "p_values": reverse_p_values,
                        "most_significant_lag": reverse_min_p_lag,
                        "has_causality": True
                    })
                else:
                    causality_results.append({
                        "variable": col,
                        "direction": f"mood → {col}",
                        "p_values": reverse_p_values,
                        "has_causality": False
                    })
                
            except Exception as e:
                # Skip if test fails
                continue
        
        # Filter to only include results with causality
        causality_results = [result for result in causality_results if result["has_causality"]]
        
        # Sort by significance
        causality_results.sort(key=lambda x: x["most_significant_lag"]["p_value"] if "most_significant_lag" in x else 1.0)
        
        # Generate insights
        insights = []
        
        for result in causality_results:
            if "most_significant_lag" in result:
                var_name = result["variable"].replace("_", " ")
                lag = result["most_significant_lag"]["lag"]
                direction = result["direction"]
                
                if "→ mood" in direction:
                    insights.append(f"Changes in {var_name} appear to precede changes in your mood by {lag} day{'s' if lag > 1 else ''}.")
                else:
                    insights.append(f"Changes in your mood appear to precede changes in {var_name} by {lag} day{'s' if lag > 1 else ''}.")
        
        return {
            "status": "success",
            "causality_results": causality_results,
            "insights": insights
        }
    
    def analyze_multivariate_relationships(self, days: int = 90) -> Dict[str, Any]:
        """
        Analyze multivariate relationships between variables using PCA and VAR models.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with multivariate analysis results and insights
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns or len(daily_df) < 14:
            return {
                "status": "insufficient_data",
                "message": "Need at least 14 days of data for multivariate analysis"
            }
        
        # Identify potential predictor columns
        predictor_cols = []
        for col in daily_df.columns:
            if col != "date" and "mood_" not in col:
                # Skip columns with all zeros or NaN
                if daily_df[col].sum() == 0 or daily_df[col].isna().all():
                    continue
                predictor_cols.append(col)
        
        if len(predictor_cols) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 predictor variables for multivariate analysis"
            }
        
        # Prepare data for analysis
        analysis_cols = ["mood_mean"] + predictor_cols
        analysis_df = daily_df[analysis_cols].copy()
        
        # Standardize the data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(analysis_df)
        scaled_df = pd.DataFrame(scaled_data, columns=analysis_cols)
        
        # Perform PCA
        pca_results = {}
        try:
            pca = PCA()
            pca.fit(scaled_data)
            
            # Get explained variance
            explained_variance = pca.explained_variance_ratio_
            
            # Get component loadings
            loadings = pca.components_
            
            # Create loadings dataframe
            loadings_df = pd.DataFrame(
                loadings.T, 
                columns=[f"PC{i+1}" for i in range(len(loadings))],
                index=analysis_cols
            )
            
            # Find variables with high loadings on same components as mood
            mood_related_vars = []
            
            # Get the component where mood has the highest loading
            mood_pc = loadings_df.loc["mood_mean"].abs().idxmax()
            mood_loading = loadings_df.loc["mood_mean", mood_pc]
            
            # Find variables with high loadings on this component
            for var in predictor_cols:
                var_loading = loadings_df.loc[var, mood_pc]
                
                # Check if the variable has a substantial loading on the same component
                if abs(var_loading) > 0.3:
                    # Check if the loading is in the same or opposite direction
                    relationship = "positive" if (var_loading * mood_loading) > 0 else "negative"
                    
                    mood_related_vars.append({
                        "variable": var,
                        "loading": float(var_loading),
                        "relationship": relationship,
                        "strength": abs(var_loading)
                    })
            
            # Sort by strength
            mood_related_vars.sort(key=lambda x: x["strength"], reverse=True)
            
            pca_results = {
                "explained_variance": [float(v) for v in explained_variance],
                "mood_principal_component": mood_pc,
                "mood_related_variables": mood_related_vars
            }
            
        except Exception as e:
            pca_results = {"error": str(e)}
        
        # Perform VAR analysis if we have enough data
        var_results = {}
        if len(daily_df) >= 30:
            try:
                # Prepare data for VAR
                var_data = scaled_df.copy()
                
                # Fit VAR model
                model = VAR(var_data)
                results = model.fit(maxlags=min(7, len(var_data) // 5))
                
                # Get Granger causality results
                granger_results = []
                for i, col in enumerate(var_data.columns):
                    if col == "mood_mean":
                        continue
                        
                    # Test if variable Granger-causes mood
                    test_result = results.test_causality("mood_mean", col, kind="f")
                    
                    if test_result.pvalue < 0.05:
                        granger_results.append({
                            "variable": col,
                            "direction": f"{col} → mood",
                            "p_value": float(test_result.pvalue),
                            "test_statistic": float(test_result.test_statistic),
                            "significant": True
                        })
                    
                    # Test if mood Granger-causes variable
                    reverse_test = results.test_causality(col, "mood_mean", kind="f")
                    
                    if reverse_test.pvalue < 0.05:
                        granger_results.append({
                            "variable": col,
                            "direction": f"mood → {col}",
                            "p_value": float(reverse_test.pvalue),
                            "test_statistic": float(reverse_test.test_statistic),
                            "significant": True
                        })
                
                # Sort by significance
                granger_results.sort(key=lambda x: x["p_value"])
                
                var_results = {
                    "model_order": results.k_ar,
                    "granger_causality": granger_results
                }
                
            except Exception as e:
                var_results = {"error": str(e)}
        
        # Generate insights
        insights = []
        
        # PCA insights
        if "mood_related_variables" in pca_results:
            for var in pca_results["mood_related_variables"][:3]:  # Top 3
                var_name = var["variable"].replace("_", " ")
                relationship = var["relationship"]
                
                if relationship == "positive":
                    insights.append(f"{var_name.title()} tends to move in the same direction as your mood.")
                else:
                    insights.append(f"{var_name.title()} tends to move in the opposite direction from your mood.")
        
        # VAR insights
        if "granger_causality" in var_results:
            for result in var_results["granger_causality"][:3]:  # Top 3
                var_name = result["variable"].replace("_", " ")
                direction = result["direction"]
                
                if "→ mood" in direction:
                    insights.append(f"Changes in {var_name} appear to predict changes in your mood.")
                else:
                    insights.append(f"Changes in your mood appear to predict changes in {var_name}.")
        
        return {
            "status": "success",
            "pca_analysis": pca_results,
            "var_analysis": var_results,
            "insights": insights
        }
    
    def analyze_mood_cycles(self, days: int = 90) -> Dict[str, Any]:
        """
        Analyze cyclical patterns in mood data.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with cycle analysis results and insights
        """
        daily_df = self._prepare_daily_dataframe(days)
        
        if "mood_mean" not in daily_df.columns or len(daily_df) < 14:
            return {
                "status": "insufficient_data",
                "message": "Need at least 14 days of data for cycle analysis"
            }
        
        # Calculate autocorrelation
        try:
            mood_data = daily_df["mood_mean"].values
            
            # Calculate autocorrelation function (ACF)
            acf_values = acf(mood_data, nlags=min(14, len(mood_data) // 2))
            
            # Calculate partial autocorrelation function (PACF)
            pacf_values = pacf(mood_data, nlags=min(14, len(mood_data) // 2))
            
            # Find significant lags in ACF
            acf_results = []
            for i, value in enumerate(acf_values):
                if i == 0:  # Skip lag 0 (correlation with itself)
                    continue
                    
                # Calculate significance threshold (95% confidence)
                threshold = 1.96 / np.sqrt(len(mood_data))
                
                acf_results.append({
                    "lag": i,
                    "correlation": float(value),
                    "significant": abs(value) > threshold
                })
            
            # Find significant lags in PACF
            pacf_results = []
            for i, value in enumerate(pacf_values):
                if i == 0:  # Skip lag 0
                    continue
                    
                # Calculate significance threshold (95% confidence)
                threshold = 1.96 / np.sqrt(len(mood_data))
                
                pacf_results.append({
                    "lag": i,
                    "correlation": float(value),
                    "significant": abs(value) > threshold
                })
            
            # Identify potential cycles
            cycles = []
            
            # Look for significant positive autocorrelations
            significant_positive_acf = [r for r in acf_results if r["significant"] and r["correlation"] > 0]
            
            if significant_positive_acf:
                # Sort by lag
                significant_positive_acf.sort(key=lambda x: x["lag"])
                
                # The first significant positive lag might indicate a cycle
                first_cycle = significant_positive_acf[0]
                cycles.append({
                    "length": first_cycle["lag"],
                    "strength": first_cycle["correlation"],
                    "type": "primary"
                })
                
                # Check for additional cycles
                for result in significant_positive_acf[1:]:
                    # Skip multiples of the first cycle
                    if result["lag"] % first_cycle["lag"] != 0:
                        cycles.append({
                            "length": result["lag"],
                            "strength": result["correlation"],
                            "type": "secondary"
                        })
            
            # Weekly cycle check
            if len(mood_data) >= 14:
                # Check specifically for 7-day cycle
                weekly_lag = min(acf_results, key=lambda x: abs(x["lag"] - 7))
                
                if weekly_lag["lag"] == 7 and weekly_lag["correlation"] > 0.2:
                    # Add weekly cycle if not already included
                    if not any(c["length"] == 7 for c in cycles):
                        cycles.append({
                            "length": 7,
                            "strength": weekly_lag["correlation"],
                            "type": "weekly"
                        })
            
            # Sort cycles by strength
            cycles.sort(key=lambda x: x["strength"], reverse=True)
            
            # Generate insights
            insights = []
            
            if cycles:
                for cycle in cycles[:2]:  # Top 2 cycles
                    cycle_length = cycle["length"]
                    cycle_type = cycle["type"]
                    
                    if cycle_length == 7:
                        insights.append("Your mood appears to follow a weekly cycle.")
                    else:
                        insights.append(f"Your mood appears to cycle approximately every {cycle_length} days.")
            else:
                insights.append("No clear cyclical patterns were detected in your mood data.")
            
            return {
                "status": "success",
                "autocorrelation": acf_results,
                "partial_autocorrelation": pacf_results,
                "cycles": cycles,
                "insights": insights
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error in cycle analysis: {str(e)}"
            }
    
    def generate_comprehensive_correlation_analysis(self, days: int = 90) -> Dict[str, Any]:
        """
        Generate a comprehensive correlation analysis combining all methods.
        
        Args:
            days: Number of days of data to analyze
            
        Returns:
            Dictionary with all analyses and insights
        """
        # Run all analyses
        lagged_correlations = self.analyze_lagged_correlations(days)
        granger_causality = self.analyze_granger_causality(days)
        multivariate_relationships = self.analyze_multivariate_relationships(days)
        mood_cycles = self.analyze_mood_cycles(days)
        
        # Compile all insights
        all_insights = []
        
        if lagged_correlations.get("status") == "success":
            all_insights.extend(lagged_correlations.get("insights", []))
        
        if granger_causality.get("status") == "success":
            all_insights.extend(granger_causality.get("insights", []))
        
        if multivariate_relationships.get("status") == "success":
            all_insights.extend(multivariate_relationships.get("insights", []))
        
        if mood_cycles.get("status") == "success":
            all_insights.extend(mood_cycles.get("insights", []))
        
        # Prioritize insights
        key_insights = []
        
        # Add cycle insights first
        cycle_insights = mood_cycles.get("insights", []) if mood_cycles.get("status") == "success" else []
        key_insights.extend(cycle_insights)
        
        # Add strongest causal relationships
        causal_insights = []
        if granger_causality.get("status") == "success":
            causal_insights = granger_causality.get("insights", [])[:2]  # Top 2
        key_insights.extend(causal_insights)
        
        # Add strongest lagged correlations
        lag_insights = []
        if lagged_correlations.get("status") == "success":
            lag_insights = lagged_correlations.get("insights", [])[:2]  # Top 2
        key_insights.extend(lag_insights)
        
        # Add multivariate insights
        multivar_insights = []
        if multivariate_relationships.get("status") == "success":
            multivar_insights = multivariate_relationships.get("insights", [])[:2]  # Top 2
        key_insights.extend(multivar_insights)
        
        # Remove duplicates while preserving order
        unique_insights = []
        for insight in key_insights:
            if insight not in unique_insights:
                unique_insights.append(insight)
        
        # Compile results
        return {
            "lagged_correlations": lagged_correlations,
            "granger_causality": granger_causality,
            "multivariate_relationships": multivariate_relationships,
            "mood_cycles": mood_cycles,
            "all_insights": all_insights,
            "key_insights": unique_insights
        }


# Example usage
if __name__ == "__main__":
    from src.data_collection import DataCollector
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
    
    # Create correlation analyzer and analyze
    analyzer = CorrelationAnalyzer(collector)
    analysis = analyzer.generate_comprehensive_correlation_analysis()
    
    # Print key insights
    print("Key Insights:")
    for i, insight in enumerate(analysis["key_insights"]):
        print(f"{i+1}. {insight}")
