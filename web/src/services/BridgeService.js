/**
 * Bridge Service
 * 
 * This service provides a standardized interface for the React web app
 * to communicate with the Node-Python bridge in the Mental Health Pattern
 * Recognition Assistant.
 */

// API base URL - replace with server URL from config if needed
const API_BASE_URL = 'http://localhost:3003';

// Default request timeout in milliseconds
const DEFAULT_TIMEOUT = 8000;

// Custom error class for bridge operations
class BridgeError extends Error {
  constructor(message, status, data = {}) {
    super(message);
    this.name = 'BridgeError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Make API request to the bridge server
 * 
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Request options
 * @returns {Promise<any>} - Response data
 * @throws {BridgeError} - If request fails
 */
async function makeRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}/${endpoint}`;
  
  // Create AbortController for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => {
    controller.abort();
  }, options.timeout || DEFAULT_TIMEOUT);
  
  try {
    // Add signal to options
    const fetchOptions = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      signal: controller.signal
    };
    
    // Make request
    const response = await fetch(url, fetchOptions);
    
    // Clear timeout
    clearTimeout(timeoutId);
    
    // Handle non-OK responses
    if (!response.ok) {
      let errorData = {};
      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, use text instead
        errorData = { message: await response.text() };
      }
      
      throw new BridgeError(
        errorData.message || `Request failed with status ${response.status}`,
        response.status,
        errorData
      );
    }
    
    // Parse response
    const data = await response.json();
    return data;
  } catch (error) {
    // Clear timeout
    clearTimeout(timeoutId);
    
    // Handle abort error (timeout)
    if (error.name === 'AbortError') {
      throw new BridgeError(
        'Request timed out',
        408,
        { timeout: options.timeout || DEFAULT_TIMEOUT }
      );
    }
    
    // Re-throw BridgeError
    if (error instanceof BridgeError) {
      throw error;
    }
    
    // Wrap other errors
    throw new BridgeError(
      error.message || 'An unknown error occurred',
      500,
      { originalError: error }
    );
  }
}

/**
 * Bridge Service API
 */
const BridgeService = {
  /**
   * Record a mood entry
   * 
   * @param {Object} moodData - Mood data to record
   * @param {number} moodData.mood_level - Mood level (1-10)
   * @param {string} moodData.notes - Notes about the mood (optional)
   * @param {string[]} moodData.emotions - Array of emotion identifiers
   * @returns {Promise<Object>} - Response with streak information
   */
  recordMood: async (moodData) => {
    try {
      const response = await makeRequest('record-mood', {
        method: 'POST',
        body: JSON.stringify(moodData)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to record mood:', error);
      throw error;
    }
  },
  
  /**
   * Record sleep data
   * 
   * @param {Object} sleepData - Sleep data to record
   * @param {string} sleepData.sleep_time - Bedtime (HH:MM format)
   * @param {string} sleepData.wake_time - Wake time (HH:MM format)
   * @param {number} sleepData.quality - Sleep quality rating (1-5)
   * @param {number} sleepData.duration - Sleep duration in hours
   * @param {number} sleepData.interruptions - Number of sleep interruptions
   * @param {string} sleepData.notes - Notes about sleep (optional)
   * @returns {Promise<Object>} - Response data
   */
  recordSleep: async (sleepData) => {
    try {
      const response = await makeRequest('record-sleep', {
        method: 'POST',
        body: JSON.stringify(sleepData)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to record sleep data:', error);
      throw error;
    }
  },
  
  /**
   * Record activity data
   * 
   * @param {Object} activityData - Activity data to record
   * @param {string} activityData.activity_type - Type of activity
   * @param {number} activityData.duration_minutes - Duration in minutes
   * @param {number} activityData.intensity - Intensity level (1-5)
   * @param {number} activityData.mood_impact - Impact on mood (-2 to 2)
   * @param {string} activityData.notes - Notes about activity (optional)
   * @returns {Promise<Object>} - Response data
   */
  recordActivity: async (activityData) => {
    try {
      const response = await makeRequest('record-activity', {
        method: 'POST',
        body: JSON.stringify(activityData)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to record activity data:', error);
      throw error;
    }
  },
  
  /**
   * Record weather data
   * 
   * @param {Object} weatherData - Weather data to record
   * @param {string} weatherData.weather_condition - Weather condition description
   * @param {number} weatherData.temperature - Temperature in Celsius
   * @param {number} weatherData.humidity - Humidity percentage
   * @param {number} weatherData.wind_speed - Wind speed
   * @param {string} weatherData.location - Location name
   * @param {Object} weatherData.coordinates - Coordinates (optional)
   * @param {number} weatherData.mood_impact - Impact on mood (-2 to 2)
   * @param {string} weatherData.notes - Notes about weather impact (optional)
   * @returns {Promise<Object>} - Response data
   */
  recordWeather: async (weatherData) => {
    try {
      const response = await makeRequest('record-weather', {
        method: 'POST',
        body: JSON.stringify(weatherData)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to record weather data:', error);
      throw error;
    }
  },
  
  /**
   * Get mood history
   * 
   * @param {Object} options - Query options
   * @param {number} options.days - Number of days to fetch (default: 30)
   * @returns {Promise<Array>} - Array of mood entries
   */
  getMoodHistory: async (options = {}) => {
    const days = options.days || 30;
    try {
      const response = await makeRequest(`mood-history?days=${days}`, {
        method: 'GET'
      });
      
      return response;
    } catch (error) {
      console.error('Failed to get mood history:', error);
      throw error;
    }
  },
  
  /**
   * Get mood statistics
   * 
   * @param {Object} options - Query options
   * @param {number} options.days - Number of days to analyze (default: 30)
   * @returns {Promise<Object>} - Mood statistics
   */
  getMoodStats: async (options = {}) => {
    const days = options.days || 30;
    try {
      const response = await makeRequest(`mood-stats?days=${days}`, {
        method: 'GET'
      });
      
      return response;
    } catch (error) {
      console.error('Failed to get mood stats:', error);
      throw error;
    }
  },
  
  /**
   * Analyze mood patterns
   * 
   * @param {Object} options - Analysis options
   * @param {number} options.days - Number of days to analyze (default: 30)
   * @returns {Promise<Object>} - Pattern analysis results
   */
  analyzePatterns: async (options = {}) => {
    const days = options.days || 30;
    try {
      const response = await makeRequest('analyze-patterns', {
        method: 'POST',
        body: JSON.stringify({ days })
      });
      
      return response;
    } catch (error) {
      console.error('Failed to analyze patterns:', error);
      throw error;
    }
  },
  
  /**
   * Generate visualization
   * 
   * @param {Object} options - Visualization options
   * @param {string} options.type - Type of visualization to generate
   * @param {number} options.days - Number of days to include (default: 30)
   * @returns {Promise<Object>} - Visualization data
   */
  generateVisualization: async (options = {}) => {
    const { type, days = 30 } = options;
    
    if (!type) {
      throw new BridgeError('Visualization type is required', 400);
    }
    
    try {
      const response = await makeRequest('generate-visualization', {
        method: 'POST',
        body: JSON.stringify({ type, days })
      });
      
      return response;
    } catch (error) {
      console.error('Failed to generate visualization:', error);
      throw error;
    }
  },
  
  /**
   * Get user settings
   * 
   * @returns {Promise<Object>} - User settings
   */
  getSettings: async () => {
    try {
      const response = await makeRequest('settings', {
        method: 'GET'
      });
      
      return response;
    } catch (error) {
      console.error('Failed to get settings:', error);
      throw error;
    }
  },
  
  /**
   * Update user settings
   * 
   * @param {Object} settings - Settings to update
   * @returns {Promise<Object>} - Updated settings
   */
  updateSettings: async (settings) => {
    try {
      const response = await makeRequest('settings', {
        method: 'PUT',
        body: JSON.stringify(settings)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to update settings:', error);
      throw error;
    }
  },
  
  /**
   * Get user achievements and progress
   * 
   * @returns {Promise<Object>} - User achievements data
   */
  getAchievements: async () => {
    try {
      const response = await makeRequest('achievements', {
        method: 'GET'
      });
      
      return response;
    } catch (error) {
      console.error('Failed to get achievements:', error);
      throw error;
    }
  },
  
  /**
   * Get comprehensive user data report
   * 
   * @param {Object} options - Report options
   * @param {number} options.days - Days to include in report (default: 90)
   * @returns {Promise<Object>} - Comprehensive data report
   */
  getComprehensiveReport: async (options = {}) => {
    const days = options.days || 90;
    
    try {
      const response = await makeRequest(`comprehensive-report?days=${days}`, {
        method: 'GET'
      });
      
      return response;
    } catch (error) {
      console.error('Failed to get comprehensive report:', error);
      throw error;
    }
  },
  
  /**
   * Export user data
   * 
   * @param {Object} options - Export options
   * @param {string} options.format - Export format ('json', 'csv', 'pdf')
   * @returns {Promise<Blob>} - Data export blob
   */
  exportData: async (options = {}) => {
    const format = options.format || 'json';
    
    try {
      const response = await makeRequest(`export-data?format=${format}`, {
        method: 'GET',
        headers: {
          'Accept': format === 'json' ? 'application/json' : 
                   format === 'csv' ? 'text/csv' : 
                   'application/pdf'
        },
        // Don't parse as JSON for blob response
        rawResponse: true
      });
      
      // Return blob
      return await response.blob();
    } catch (error) {
      console.error('Failed to export data:', error);
      throw error;
    }
  },
  
  /**
   * Check server health/status
   * 
   * @returns {Promise<Object>} - Server health info
   */
  checkHealth: async () => {
    try {
      const response = await makeRequest('health', {
        method: 'GET',
        timeout: 5000 // Shorter timeout for health check
      });
      
      return response;
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        status: 'error',
        message: error.message
      };
    }
  },
  
  /**
   * Connect to backend service
   * 
   * @returns {Promise<boolean>} - True if connection successful
   */
  connect: async () => {
    try {
      await BridgeService.checkHealth();
      return true;
    } catch (error) {
      console.error('Failed to connect to backend:', error);
      return false;
    }
  }
};

export default BridgeService;
export { BridgeError };
