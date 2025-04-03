/**
 * Mood API Routes
 * 
 * Handles all mood-related API endpoints.
 */

const express = require('express');
const router = express.Router();
const moodController = require('../controllers/moodController');

// Get all mood entries
router.get('/', moodController.getAllMoodEntries);

// Get mood entries by date range
router.get('/range', moodController.getMoodEntriesByDateRange);

// Get mood entry by ID
router.get('/:id', moodController.getMoodEntryById);

// Create a new mood entry
router.post('/', moodController.createMoodEntry);

// Update a mood entry
router.put('/:id', moodController.updateMoodEntry);

// Delete a mood entry
router.delete('/:id', moodController.deleteMoodEntry);

// Get mood statistics
router.get('/stats/summary', moodController.getMoodStatistics);

module.exports = router;
