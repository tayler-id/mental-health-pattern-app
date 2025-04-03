/**
 * Data Service
 * 
 * Provides functions for accessing and manipulating data.
 */

const pythonBridge = require('./pythonBridge');

/**
 * Get all entries of a specific type
 * 
 * @param {string} entryType - Type of entries to retrieve (e.g., 'mood_entries')
 * @returns {Promise<Array>} - Promise resolving to an array of entries
 */
exports.getAllEntries = async (entryType) => {
  return pythonBridge.callPythonFunction('get_all_entries', { entry_type: entryType });
};

/**
 * Get entries by date range
 * 
 * @param {string} entryType - Type of entries to retrieve
 * @param {string} startDate - Start date in ISO format
 * @param {string} endDate - End date in ISO format
 * @returns {Promise<Array>} - Promise resolving to an array of entries
 */
exports.getEntriesByDateRange = async (entryType, startDate, endDate) => {
  return pythonBridge.callPythonFunction('get_entries_by_date_range', {
    entry_type: entryType,
    start_date: startDate,
    end_date: endDate
  });
};

/**
 * Get entry by ID
 * 
 * @param {string} entryType - Type of entry to retrieve
 * @param {string} id - ID of the entry
 * @returns {Promise<object|null>} - Promise resolving to the entry or null if not found
 */
exports.getEntryById = async (entryType, id) => {
  return pythonBridge.callPythonFunction('get_entry_by_id', {
    entry_type: entryType,
    id
  });
};

/**
 * Get statistics for a specific entry type
 * 
 * @param {string} entryType - Type of entries to analyze
 * @param {number} days - Number of days to include in the analysis
 * @returns {Promise<object>} - Promise resolving to statistics object
 */
exports.getStatistics = async (entryType, days = 30) => {
  return pythonBridge.callPythonFunction('get_statistics', {
    entry_type: entryType,
    days
  });
};

/**
 * Export data to a file
 * 
 * @param {string} format - Format to export (e.g., 'json', 'csv')
 * @returns {Promise<string>} - Promise resolving to the path of the exported file
 */
exports.exportData = async (format = 'json') => {
  return pythonBridge.callPythonFunction('export_data', { format });
};

/**
 * Import data from a file
 * 
 * @param {string} filePath - Path to the file to import
 * @returns {Promise<boolean>} - Promise resolving to true if import was successful
 */
exports.importData = async (filePath) => {
  return pythonBridge.callPythonFunction('import_data', { file_path: filePath });
};
