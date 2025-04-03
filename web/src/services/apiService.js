/**
 * API Service
 * 
 * Provides functions for communicating with the backend API.
 */

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage = errorData.error?.message || `API error: ${response.status}`;
    throw new Error(errorMessage);
  }
  
  return response.json();
};

// Helper function to format query parameters
const formatQueryParams = (params) => {
  const queryParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      queryParams.append(key, value);
    }
  });
  
  return queryParams.toString();
};

// API service object
export const apiService = {
  // Mood endpoints
  
  /**
   * Get all mood entries
   * @param {number} days - Number of days to retrieve (optional)
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getMoodEntries: async (days) => {
    const queryParams = days ? `?${formatQueryParams({ days })}` : '';
    const response = await fetch(`${API_BASE_URL}/mood${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Get mood entries by date range
   * @param {string} startDate - Start date in ISO format
   * @param {string} endDate - End date in ISO format
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getMoodEntriesByDateRange: async (startDate, endDate) => {
    const queryParams = formatQueryParams({ startDate, endDate });
    const response = await fetch(`${API_BASE_URL}/mood/range?${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Get mood entry by ID
   * @param {string} id - Mood entry ID
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getMoodEntryById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/mood/${id}`);
    return handleResponse(response);
  },
  
  /**
   * Create a new mood entry
   * @param {Object} moodData - Mood entry data
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  createMoodEntry: async (moodData) => {
    const response = await fetch(`${API_BASE_URL}/mood`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(moodData)
    });
    
    return handleResponse(response);
  },
  
  /**
   * Update a mood entry
   * @param {string} id - Mood entry ID
   * @param {Object} moodData - Updated mood entry data
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  updateMoodEntry: async (id, moodData) => {
    const response = await fetch(`${API_BASE_URL}/mood/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(moodData)
    });
    
    return handleResponse(response);
  },
  
  /**
   * Delete a mood entry
   * @param {string} id - Mood entry ID
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  deleteMoodEntry: async (id) => {
    const response = await fetch(`${API_BASE_URL}/mood/${id}`, {
      method: 'DELETE'
    });
    
    return handleResponse(response);
  },
  
  /**
   * Get mood statistics
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getMoodStatistics: async (days = 30) => {
    const queryParams = formatQueryParams({ days });
    const response = await fetch(`${API_BASE_URL}/mood/stats/summary?${queryParams}`);
    return handleResponse(response);
  },
  
  // Activity endpoints
  
  /**
   * Get all activity entries
   * @param {number} days - Number of days to retrieve (optional)
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getActivityEntries: async (days) => {
    const queryParams = days ? `?${formatQueryParams({ days })}` : '';
    const response = await fetch(`${API_BASE_URL}/activity${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Create a new activity entry
   * @param {Object} activityData - Activity entry data
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  createActivityEntry: async (activityData) => {
    const response = await fetch(`${API_BASE_URL}/activity`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(activityData)
    });
    
    return handleResponse(response);
  },
  
  // Sleep endpoints
  
  /**
   * Get all sleep entries
   * @param {number} days - Number of days to retrieve (optional)
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getSleepEntries: async (days) => {
    const queryParams = days ? `?${formatQueryParams({ days })}` : '';
    const response = await fetch(`${API_BASE_URL}/sleep${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Create a new sleep entry
   * @param {Object} sleepData - Sleep entry data
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  createSleepEntry: async (sleepData) => {
    const response = await fetch(`${API_BASE_URL}/sleep`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sleepData)
    });
    
    return handleResponse(response);
  },
  
  // Analysis endpoints
  
  /**
   * Run pattern recognition
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  runPatternRecognition: async (days = 90) => {
    const response = await fetch(`${API_BASE_URL}/analysis/patterns`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ days })
    });
    
    return handleResponse(response);
  },
  
  /**
   * Run correlation analysis
   * @param {number} days - Number of days to analyze
   * @param {string} analysisType - Type of analysis ('activity', 'sleep', or 'all')
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  runCorrelationAnalysis: async (days = 90, analysisType = 'all') => {
    const response = await fetch(`${API_BASE_URL}/analysis/correlations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ days, analysisType })
    });
    
    return handleResponse(response);
  },
  
  /**
   * Get mood patterns
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getMoodPatterns: async (days = 90) => {
    const queryParams = formatQueryParams({ days });
    const response = await fetch(`${API_BASE_URL}/analysis/patterns/mood?${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Get activity-mood correlations
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getActivityMoodCorrelations: async (days = 90) => {
    const queryParams = formatQueryParams({ days });
    const response = await fetch(`${API_BASE_URL}/analysis/correlations/activity-mood?${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Get sleep-mood correlations
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getSleepMoodCorrelations: async (days = 90) => {
    const queryParams = formatQueryParams({ days });
    const response = await fetch(`${API_BASE_URL}/analysis/correlations/sleep-mood?${queryParams}`);
    return handleResponse(response);
  },
  
  /**
   * Get comprehensive analysis
   * @param {number} days - Number of days to analyze
   * @returns {Promise<Object>} - Promise resolving to the API response
   */
  getComprehensiveAnalysis: async (days = 90) => {
    const queryParams = formatQueryParams({ days });
    const response = await fetch(`${API_BASE_URL}/analysis/comprehensive?${queryParams}`);
    return handleResponse(response);
  },
  
  // Visualization endpoints
  
  /**
   * Generate mood timeline visualization
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateMoodTimeline: async (days = 30, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/mood-timeline?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  },
  
  /**
   * Generate mood by day of week visualization
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateMoodByDayOfWeek: async (days = 90, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/mood-by-day?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  },
  
  /**
   * Generate emotion distribution visualization
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateEmotionDistribution: async (days = 90, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/emotion-distribution?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  },
  
  /**
   * Generate activity-mood correlation visualization
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateActivityMoodCorrelation: async (days = 90, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/activity-mood?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  },
  
  /**
   * Generate sleep-mood correlation visualization
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateSleepMoodCorrelation: async (days = 90, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/sleep-mood?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  },
  
  /**
   * Generate dashboard
   * @param {number} days - Number of days to include
   * @param {string} format - Format of the visualization ('json' or 'image')
   * @returns {Promise<Object|Blob>} - Promise resolving to the API response
   */
  generateDashboard: async (days = 90, format = 'json') => {
    const queryParams = formatQueryParams({ days, format });
    const response = await fetch(`${API_BASE_URL}/visualization/dashboard?${queryParams}`);
    
    if (format === 'image') {
      return response.blob();
    }
    
    return handleResponse(response);
  }
};
