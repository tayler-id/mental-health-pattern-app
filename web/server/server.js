/**
 * Express Server for Mental Health Pattern Recognition Web UI
 * 
 * This server provides RESTful API endpoints that interface with the
 * Mental Health Pattern Recognition CLI application.
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');

// Import routes
const moodRoutes = require('./routes/mood');
const activityRoutes = require('./routes/activity');
const sleepRoutes = require('./routes/sleep');
const analysisRoutes = require('./routes/analysis');
const visualizationRoutes = require('./routes/visualization');

// Create Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '../build')));

// Log requests
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// API Routes
app.use('/api/mood', moodRoutes);
app.use('/api/activity', activityRoutes);
app.use('/api/sleep', sleepRoutes);
app.use('/api/analysis', analysisRoutes);
app.use('/api/visualization', visualizationRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve React app for any other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: {
      message: 'An error occurred on the server',
      details: process.env.NODE_ENV === 'development' ? err.message : undefined
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API available at http://localhost:${PORT}/api`);
});

module.exports = app;
