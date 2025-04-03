/**
 * Visualization API Routes
 * 
 * Handles all visualization-related API endpoints.
 */

const express = require('express');
const router = express.Router();
const visualizationController = require('../controllers/visualizationController');

// Generate mood timeline visualization
router.get('/mood-timeline', visualizationController.generateMoodTimeline);

// Generate mood by day of week visualization
router.get('/mood-by-day', visualizationController.generateMoodByDayOfWeek);

// Generate emotion distribution visualization
router.get('/emotion-distribution', visualizationController.generateEmotionDistribution);

// Generate activity-mood correlation visualization
router.get('/activity-mood', visualizationController.generateActivityMoodCorrelation);

// Generate sleep-mood correlation visualization
router.get('/sleep-mood', visualizationController.generateSleepMoodCorrelation);

// Generate pattern visualization
router.get('/patterns', visualizationController.generatePatternVisualization);

// Generate dashboard
router.get('/dashboard', visualizationController.generateDashboard);

module.exports = router;
