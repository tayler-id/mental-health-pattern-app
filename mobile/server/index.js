const express = require('express');
const { PythonShell } = require('python-shell');
const app = express();

// Enable CORS for cross-origin requests between React app and server
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  next();
});

app.use(express.json());
// Record mood data
app.post('/record-mood', (req, res) => {
  console.log('Received /record-mood request:', req.body);
  const { mood_level, notes, emotions, streak } = req.body;
  const newStreak = Math.min((streak || 0) + 1, 7); // Cap at 7 and handle undefined streak
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: [
      mood_level || 5,  // Default to neutral (5) if no mood level provided
      notes || '',
      JSON.stringify(emotions || []),
      newStreak
    ]
  };
  
  console.log('Executing python_bridge.py with options:', options);
  
  // Use our bridge script to handle the Python execution
  PythonShell.run('python_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message, 
        details: 'Error executing Python bridge script'
      });
    }
    
    // Check for Python script results
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    console.log('Python script completed successfully, sending response:', { success: true, streak: newStreak });
    res.json({ success: true, streak: newStreak });
  });
});

// Get mood data
app.get('/mood-data', (req, res) => {
  console.log('Received /mood-data request');
  const { days, page, per_page } = req.query;
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: [
      'get_mood_data',
      days || '30',
      page || '1',
      per_page || '10'
    ]
  };
  
  PythonShell.run('data_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message
      });
    }
    
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    res.json(pythonResult || { success: false, error: 'No data returned' });
  });
});

// Get analysis
app.get('/analysis', (req, res) => {
  console.log('Received /analysis request');
  const { type, days } = req.query;
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: [
      'analyze_patterns',
      type || 'mood',
      days || '30'
    ]
  };
  
  PythonShell.run('analysis_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message
      });
    }
    
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    res.json(pythonResult || { success: false, error: 'No analysis data returned' });
  });
});

// Get visualizations
app.get('/visualizations', (req, res) => {
  console.log('Received /visualizations request');
  const { type, days } = req.query;
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: [
      'generate_visualization',
      type || 'mood_timeline',
      days || '30'
    ]
  };
  
  PythonShell.run('visualization_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message
      });
    }
    
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    res.json(pythonResult || { success: false, error: 'No visualization data returned' });
  });
});

// Get and update settings
app.get('/settings', (req, res) => {
  console.log('Received /settings GET request');
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: ['get_settings']
  };
  
  PythonShell.run('settings_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message
      });
    }
    
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    res.json(pythonResult || { success: false, error: 'No settings data returned' });
  });
});

app.post('/settings', (req, res) => {
  console.log('Received /settings POST request:', req.body);
  const settings = req.body;
  
  const options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: 'mobile/server',
    args: [
      'update_settings',
      JSON.stringify(settings || {})
    ]
  };
  
  PythonShell.run('settings_bridge.py', options, (err, results) => {
    if (err) {
      console.error('Python execution failed:', err);
      return res.status(500).json({ 
        success: false, 
        error: err.message
      });
    }
    
    const pythonResult = results && results.length > 0 ? results[0] : null;
    if (pythonResult && !pythonResult.success) {
      console.error('Python script reported an error:', pythonResult.error);
      return res.status(500).json({ success: false, error: pythonResult.error });
    }
    
    res.json(pythonResult || { success: false, error: 'Settings could not be updated' });
  });
});
app.listen(3001, () => console.log('Server running on port 3001')); // Changed from 3000 to avoid conflict with React dev server
