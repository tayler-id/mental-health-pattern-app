/**
 * Analysis API Routes
 * 
 * Handles all analysis-related API endpoints.
 */

const express = require('express');
const router = express.Router();
const analysisController = require('../controllers/analysisController');

// Run pattern recognition
router.post('/patterns', analysisController.runPatternRecognition);

// Run correlation analysis
router.post('/correlations', analysisController.runCorrelationAnalysis);

// Get mood patterns
router.get('/patterns/mood', analysisController.getMoodPatterns);

// Get activity-mood correlations
router.get('/correlations/activity-mood', analysisController.getActivityMoodCorrelations);

// Get sleep-mood correlations
router.get('/correlations/sleep-mood', analysisController.getSleepMoodCorrelations);

// Get comprehensive analysis
router.get('/comprehensive', analysisController.getComprehensiveAnalysis);

module.exports = router;
