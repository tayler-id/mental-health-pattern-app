# API Integration Guide for Mental Health Tracker Web App

This document outlines the necessary API endpoints, their implementations, and integration requirements for the Mental Health Tracker web application.

## Current API Endpoint

### 1. Record Mood
- **Endpoint**: `POST /record-mood`
- **Server**: Node.js server on port 3001
- **Purpose**: Record user mood data with associated emotions and notes
- **Status**: Implemented but needs CORS configuration

## Required Additional Endpoints

To fully implement the application, the following endpoints need to be developed:

### 2. View Data
- **Endpoint**: `GET /mood-data`
- **Purpose**: Retrieve user's recorded mood data
- **Implementation Needs**:
  - Add route to express server
  - Create Python script to fetch data from storage
  - Return formatted mood entries with pagination support
  - Apply proper error handling and CORS headers

### 3. Run Analysis
- **Endpoint**: `GET /analysis`
- **Purpose**: Generate analysis of user's mood patterns
- **Implementation Needs**:
  - Implement pattern recognition algorithms in Python
  - Connect to Node.js endpoint
  - Support parameters for different analysis types (time-based, correlation, etc.)
  - Return analysis results in structured JSON format

### 4. Generate Visualizations
- **Endpoint**: `GET /visualizations`
- **Purpose**: Create visual representations of mood data
- **Implementation Needs**:
  - Implement Python script to generate visualizations
  - Return image data or visualization configuration for client-side rendering
  - Support different visualization types (mood timeline, emotion distribution, etc.)

### 5. User Settings
- **Endpoint**: `GET/POST /settings`
- **Purpose**: Retrieve and update user preferences
- **Implementation Needs**:
  - Create storage for user settings
  - Implement CRUD operations for settings

## Integration Guide

### Node.js Server Integration

1. Add these routes to the server:

```javascript
// Get mood data
app.get('/mood-data', (req, res) => {
  // Implementation similar to record-mood endpoint
  // Use PythonShell to run data retrieval script
});

// Get analysis
app.get('/analysis', (req, res) => {
  const { analysisType } = req.query;
  // Run appropriate Python analysis script
});

// Get visualizations
app.get('/visualizations', (req, res) => {
  const { visType } = req.query;
  // Run Python script to generate visualization
});

// Get/Update settings
app.get('/settings', (req, res) => {
  // Retrieve user settings
});

app.post('/settings', (req, res) => {
  // Update user settings
});
```

### Python Script Integration

For each endpoint, create corresponding Python functions in the appropriate modules:

1. **Data Retrieval** in `data_collection.py`:
   ```python
   def get_mood_data(days=30, page=1, per_page=10):
       # Retrieve mood data with pagination
   ```

2. **Analysis Functions** in `pattern_recognition.py`:
   ```python
   def analyze_patterns(data_type, days=30):
       # Analyze patterns based on data type
   ```

3. **Visualization Functions** in `visualization.py`:
   ```python
   def generate_visualization(vis_type, days=30):
       # Generate visualization based on type
   ```

### React Frontend Integration

Update the React components to call these new endpoints:

1. **View Data Component**:
   ```javascript
   const fetchMoodData = async (page = 1) => {
     const response = await fetch(`${serverUrl.replace('/record-mood', '/mood-data')}?page=${page}`);
     // Process and display data
   };
   ```

2. **Analysis Component**:
   ```javascript
   const runAnalysis = async (analysisType) => {
     const response = await fetch(`${serverUrl.replace('/record-mood', '/analysis')}?type=${analysisType}`);
     // Process and display analysis
   };
   ```

3. **Visualization Component**:
   ```javascript
   const getVisualization = async (visType) => {
     const response = await fetch(`${serverUrl.replace('/record-mood', '/visualizations')}?type=${visType}`);
     // Process and display visualization
   };
   ```

## Error Handling and CORS

Ensure all endpoints have proper error handling and CORS configuration:

```javascript
// Error middleware (add after all routes)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ 
    success: false, 
    error: err.message || 'An unexpected error occurred'
  });
});

// CORS middleware is already configured globally in the application
```

## Testing Procedure

1. Start the Node.js server on port 3001
2. Start the React application on port 3000
3. Test each endpoint with different parameters
4. Verify data is correctly displayed in the UI

## Future Enhancements

1. **WebSocket Integration** for real-time updates
2. **Authentication System** for multi-user support
3. **Offline Mode** with local storage and synchronization
4. **Advanced Analytics** with machine learning components
