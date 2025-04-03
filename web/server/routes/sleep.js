/**
 * Sleep API Routes
 * 
 * Handles all sleep-related API endpoints.
 */

const express = require('express');
const router = express.Router();
const sleepController = require('../controllers/sleepController');

// Get all sleep entries
router.get('/', sleepController.getAllSleepEntries);

// Get sleep entries by date range
router.get('/range', sleepController.getSleepEntriesByDateRange);

// Get sleep entry by ID
router.get('/:id', sleepController.getSleepEntryById);

// Create a new sleep entry
router.post('/', sleepController.createSleepEntry);

// Update a sleep entry
router.put('/:id', sleepController.updateSleepEntry);

// Delete a sleep entry
router.delete('/:id', sleepController.deleteSleepEntry);

// Get sleep statistics
router.get('/stats/summary', sleepController.getSleepStatistics);

module.exports = router;
