/**
 * Activity API Routes
 * 
 * Handles all activity-related API endpoints.
 */

const express = require('express');
const router = express.Router();
const activityController = require('../controllers/activityController');

// Get all activity entries
router.get('/', activityController.getAllActivityEntries);

// Get activity entries by date range
router.get('/range', activityController.getActivityEntriesByDateRange);

// Get activity entry by ID
router.get('/:id', activityController.getActivityEntryById);

// Create a new activity entry
router.post('/', activityController.createActivityEntry);

// Update an activity entry
router.put('/:id', activityController.updateActivityEntry);

// Delete an activity entry
router.delete('/:id', activityController.deleteActivityEntry);

// Get activity statistics
router.get('/stats/summary', activityController.getActivityStatistics);

module.exports = router;
