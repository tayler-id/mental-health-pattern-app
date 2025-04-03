/**
 * Visualization Controller
 * 
 * Handles all visualization-related API requests.
 */

const pythonBridge = require('../services/pythonBridge');
const path = require('path');
const fs = require('fs');

/**
 * Generate mood timeline visualization
 */
exports.generateMoodTimeline = async (req, res, next) => {
  try {
    const { days = 30, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_mood_timeline', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_mood_timeline_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate mood by day of week visualization
 */
exports.generateMoodByDayOfWeek = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_mood_by_day_of_week', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_mood_by_day_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate emotion distribution visualization
 */
exports.generateEmotionDistribution = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_emotion_distribution', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_emotion_distribution_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate activity-mood correlation visualization
 */
exports.generateActivityMoodCorrelation = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_mood_activity_correlation', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_activity_mood_correlation_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate sleep-mood correlation visualization
 */
exports.generateSleepMoodCorrelation = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_mood_sleep_correlation', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_sleep_mood_correlation_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate pattern visualization
 */
exports.generatePatternVisualization = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_pattern_visualization', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Visualization image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_pattern_visualization_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};

/**
 * Generate dashboard
 */
exports.generateDashboard = async (req, res, next) => {
  try {
    const { days = 90, format = 'json' } = req.query;
    
    if (format === 'image') {
      // Generate image visualization
      const imagePath = await pythonBridge.callPythonFunction('generate_dashboard', {
        days: parseInt(days, 10)
      });
      
      // Check if file exists
      if (!fs.existsSync(imagePath)) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Dashboard image not found'
          }
        });
      }
      
      // Send image file
      res.sendFile(path.resolve(imagePath));
    } else {
      // Generate data for client-side visualization
      const data = await pythonBridge.callPythonFunction('get_dashboard_data', {
        days: parseInt(days, 10)
      });
      
      res.json({
        success: true,
        data
      });
    }
  } catch (error) {
    next(error);
  }
};
