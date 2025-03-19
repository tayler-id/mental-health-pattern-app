
# Mental Health Pattern Recognition Assistant - Project Rules

## Code Organization Patterns

1. **Module Structure**: Each major component has its own dedicated module file in the `src` directory.
   - `data_collection.py`: Core data storage and retrieval
   - `mood_tracking.py`: Mood-specific functionality
   - `pattern_recognition.py`: Pattern identification algorithms
   - `correlation_analysis.py`: Statistical correlation analysis
   - `visualization.py`: Visualization generation
   - `user_interface.py`: Command-line interface

2. **Class Naming Convention**: Main component classes follow a descriptive naming pattern:
   - `DataCollector`: Handles data collection and storage
   - `MoodTracker`: Manages mood tracking functionality
   - `PatternRecognitionEngine`: Implements pattern recognition algorithms
   - `CorrelationAnalyzer`: Performs correlation analysis
   - `VisualizationGenerator`: Creates visualizations
   - `UserInterface`: Manages user interaction

3. **Method Naming Patterns**:
   - Data retrieval methods use `get_*` prefix (e.g., `get_mood_history`)
   - Data recording methods use `record_*` prefix (e.g., `record_mood`)
   - Analysis methods use `analyze_*` or `identify_*` prefix (e.g., `identify_mood_patterns`)
   - Visualization methods use `generate_*` prefix (e.g., `generate_mood_timeline`)
   - Comprehensive methods use `generate_comprehensive_*` prefix (e.g., `generate_comprehensive_analysis`)

4. **Directory Structure**:
   - `data/`: Storage for user data and exports
   - `src/`: Source code modules
   - `tests/`: Test files
   - `visualization/`: Output directory for generated visualizations
   - `models/`: Reserved for future machine learning models
   - `ui/`: Reserved for future UI components

## Implementation Patterns

1. **Dependency Injection**: Components accept their dependencies through constructors, with default instantiation if not provided:
   ```python
   def __init__(self, data_collector: Optional[DataCollector] = None):
       self.data_collector = data_collector or DataCollector()
   ```

2. **Error Handling**: Components return status dictionaries rather than raising exceptions for expected error conditions:
   ```python
   return {
       "status": "insufficient_data",
       "message": "Not enough data for analysis"
   }
   ```

3. **Data Structure**: User data is stored in a structured JSON format with the following top-level keys:
   - `mood_entries`: List of mood data points
   - `activity_entries`: List of activity records
   - `sleep_entries`: List of sleep records
   - `medication_entries`: List of medication records
   - `custom_entries`: List of user-defined data points
   - `user_settings`: User configuration options

4. **Timestamp Format**: All timestamps use ISO format (YYYY-MM-DDTHH:MM:SS) for consistency and easy sorting:
   ```python
   timestamp = datetime.datetime.now().isoformat()
   ```

5. **Visualization Output**: Visualizations are saved as PNG files in subdirectories of the `visualization` directory:
   - `mood/`: Mood-related visualizations
   - `patterns/`: Pattern visualizations
   - `correlations/`: Correlation visualizations
   - `dashboards/`: Comprehensive dashboards

## Analysis Patterns

1. **Data Preparation**: Analysis components first prepare a daily aggregated DataFrame from raw data:
   ```python
   daily_df = self._prepare_daily_dataframe(days)
   ```

2. **Insight Generation**: Analysis results include an `insights` list with human-readable interpretations:
   ```python
   return {
       "status": "success",
       "data": analysis_results,
       "insights": insights
   }
   ```

3. **Minimum Data Requirements**:
   - Pattern recognition requires at least 7 days of data
   - Correlation analysis works best with 30+ days of data
   - Advanced analyses (causality, cycles) need 60+ days of data

4. **Analysis Result Structure**: Analysis results follow a consistent structure:
   - `status`: Success or error status
   - Data-specific results (varies by analysis type)
   - `insights`: List of human-readable insights

## User Interface Patterns

1. **Menu Structure**: The command-line interface uses a hierarchical menu structure:
   - Main Menu → Category Menu → Action Menu
   - Each menu provides numbered options and clear navigation

2. **Color Coding**: The interface uses consistent color coding for different types of information:
   - Titles: Bold cyan
   - Success messages: Bold green
   - Error messages: Bold red
   - Warnings: Bold yellow
   - Prompts: Bold blue

3. **Data Presentation**: Tabular data is displayed using the `tabulate` library with the "grid" format:
   ```python
   print(tabulate(table_data, headers=headers, tablefmt="grid"))
   ```

4. **User Guidance**: The interface provides clear guidance on data requirements and interpretation:
   - Warnings when insufficient data is available
   - Explanations of analysis results
   - Suggestions for data collection to improve analysis quality

## Visualization Patterns

1. **Color Scheme**: Visualizations use a consistent color scheme:
   - High mood: Green (#2ecc71)
   - Medium mood: Blue (#3498db)
   - Low mood: Red (#e74c3c)
   - Neutral elements: Gray (#95a5a6)

2. **Layout Structure**: Complex visualizations (like dashboards) use a grid-based layout:
   ```python
   gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
   ```

3. **Annotation**: Visualizations include clear annotations:
   - Titles and axis labels
   - Data point values where appropriate
   - Trend lines and statistical indicators
   - Legend for color coding

4. **Insight Presentation**: Visualizations include text-based insights when possible:
   ```python
   ax.text(0.1, y_pos, f"• {insight}", fontsize=12, 
          ha="left", va="top", transform=ax.transAxes)
   ```

## Project-Specific Conventions

1. **Emotion Categories**: Emotions are categorized into three groups:
   - Positive: happy, content, excited, grateful, relaxed, etc.
   - Negative: sad, anxious, stressed, angry, frustrated, etc.
   - Neutral: calm, focused, contemplative, curious, etc.

2. **Mood Scale**: Mood is measured on a 1-10 scale:
   - 1-3: Low mood
   - 4-7: Medium mood
   - 8-10: High mood

3. **Analysis Timeframes**: Standard analysis timeframes are:
   - 7 days: Recent trends
   - 30 days: Monthly patterns
   - 90 days: Seasonal patterns
   - 180 days: Half-year analysis
   - 365 days: Annual patterns

4. **Correlation Strength Interpretation**:
   - 0.0-0.2: Negligible correlation
   - 0.2-0.4: Weak correlation
   - 0.4-0.6: Moderate correlation
   - 0.6-0.8: Strong correlation
   - 0.8-1.0: Very strong correlation

## Development Workflow

1. **Feature Implementation Process**:
   - Implement core functionality in the appropriate module
   - Add necessary methods to the UserInterface class
   - Create visualization support if needed
   - Update documentation to reflect new features

2. **Testing Approach**:
   - Unit tests for individual components
   - Integration tests for component interactions
   - Test with demo data for end-to-end validation

3. **Documentation Requirements**:
   - Update memory bank files when adding significant features
   - Document all public methods with docstrings
   - Include examples for complex functionality
   - Update .clinerules with new patterns or conventions

## Known Quirks and Workarounds

1. **Date Handling**: When working with dates, always convert to datetime objects before comparison:
   ```python
   # Convert string timestamps to datetime for comparison
   entry_date = datetime.datetime.fromisoformat(entry["timestamp"])
   ```

2. **Visualization Memory Usage**: When generating multiple visualizations, close figure objects to prevent memory leaks:
   ```python
   plt.savefig(save_path)
   plt.close(fig)  # Important to prevent memory leaks
   ```

3. **JSON Data Structure**: The JSON data structure uses lists for entries, which requires linear search for updates:
   ```python
   # To update an entry, you need to find it first
   for i, entry in enumerate(self.user_data["mood_entries"]):
       if entry["timestamp"] == timestamp:
           self.user_data["mood_entries"][i] = updated_entry
           break
   ```

4. **Pandas DataFrame Handling**: When working with potentially empty DataFrames, always check before operations:
   ```python
   if not df.empty and "column_name" in df.columns:
       # Proceed with operations
   ```

5. **Color Support in Terminal**: The colored output in the terminal interface may not work in all environments. The code includes fallbacks:
   ```python
   # Color codes are defined with fallbacks
   self.colors = {
       "reset": "\033[0m" if color_support else "",
       "bold": "\033[1m" if color_support else "",
       # ...
   }
