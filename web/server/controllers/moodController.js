/**
 * Mood Controller
 * 
 * Handles all mood-related API requests.
 */

const pythonBridge = require('../services/pythonBridge');
const dataService = require('../services/dataService');

/**
 * Get all mood entries
 */
exports.getAllMoodEntries = async (req, res, next) => {
  try {
    const moodEntries = await dataService.getAllEntries('mood_entries');
    res.json({
      success: true,
      data: moodEntries
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get mood entries by date range
 */
exports.getMoodEntriesByDateRange = async (req, res, next) => {
  try {
    const { startDate, endDate } = req.query;
    const moodEntries = await dataService.getEntriesByDateRange('mood_entries', startDate, endDate);
    res.json({
      success: true,
      data: moodEntries
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get mood entry by ID
 */
exports.getMoodEntryById = async (req, res, next) => {
  try {
    const { id } = req.params;
    const moodEntry = await dataService.getEntryById('mood_entries', id);
    
    if (!moodEntry) {
      return res.status(404).json({
        success: false,
        error: {
          message: `Mood entry with ID ${id} not found`
        }
      });
    }
    
    res.json({
      success: true,
      data: moodEntry
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Create a new mood entry
 */
exports.createMoodEntry = async (req, res, next) => {
  try {
    const { mood_level, notes, emotions, timestamp } = req.body;
    
    // Validate required fields
    if (!mood_level) {
      return res.status(400).json({
        success: false,
        error: {
          message: 'Mood level is required'
        }
      });
    }
    
    // Create mood entry
    const newEntry = await pythonBridge.callPythonFunction('record_mood', {
      mood_level,
      notes: notes || '',
      emotions: emotions || [],
      timestamp: timestamp || new Date().toISOString()
    });
    
    res.status(201).json({
      success: true,
      data: newEntry
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Update a mood entry
 */
exports.updateMoodEntry = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { mood_level, notes, emotions, timestamp } = req.body;
    
    // Check if entry exists
    const existingEntry = await dataService.getEntryById('mood_entries', id);
    if (!existingEntry) {
      return res.status(404).json({
        success: false,
        error: {
          message: `Mood entry with ID ${id} not found`
        }
      });
    }
    
    // Update entry
    const updatedEntry = await pythonBridge.callPythonFunction('update_mood', {
      id,
      mood_level,
      notes,
      emotions,
      timestamp
    });
    
    res.json({
      success: true,
      data: updatedEntry
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Delete a mood entry
 */
exports.deleteMoodEntry = async (req, res, next) => {
  try {
    const { id } = req.params;
    
    // Check if entry exists
    const existingEntry = await dataService.getEntryById('mood_entries', id);
    if (!existingEntry) {
      return res.status(404).json({
        success: false,
        error: {
          message: `Mood entry with ID ${id} not found`
        }
      });
    }
    
    // Delete entry
    await pythonBridge.callPythonFunction('delete_entry', {
      entry_type: 'mood_entries',
      id
    });
    
    res.json({
      success: true,
      message: `Mood entry with ID ${id} deleted successfully`
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get mood statistics
 */
exports.getMoodStatistics = async (req, res, next) => {
  try {
    const { days = 30 } = req.query;
    
    const stats = await pythonBridge.callPythonFunction('get_mood_statistics', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    next(error);
  }
};
