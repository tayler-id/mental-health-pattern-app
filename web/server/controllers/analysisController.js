/**
 * Analysis Controller
 * 
 * Handles all analysis-related API requests.
 */

const pythonBridge = require('../services/pythonBridge');

/**
 * Run pattern recognition
 */
exports.runPatternRecognition = async (req, res, next) => {
  try {
    const { days = 90 } = req.body;
    
    const result = await pythonBridge.callPythonFunction('identify_mood_patterns', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Run correlation analysis
 */
exports.runCorrelationAnalysis = async (req, res, next) => {
  try {
    const { days = 90, analysisType = 'all' } = req.body;
    
    let result;
    
    if (analysisType === 'activity') {
      result = await pythonBridge.callPythonFunction('identify_activity_mood_correlations', {
        days: parseInt(days, 10)
      });
    } else if (analysisType === 'sleep') {
      result = await pythonBridge.callPythonFunction('identify_sleep_mood_correlations', {
        days: parseInt(days, 10)
      });
    } else {
      // Run all analyses
      const activityCorrelations = await pythonBridge.callPythonFunction('identify_activity_mood_correlations', {
        days: parseInt(days, 10)
      });
      
      const sleepCorrelations = await pythonBridge.callPythonFunction('identify_sleep_mood_correlations', {
        days: parseInt(days, 10)
      });
      
      result = {
        activity: activityCorrelations,
        sleep: sleepCorrelations
      };
    }
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get mood patterns
 */
exports.getMoodPatterns = async (req, res, next) => {
  try {
    const { days = 90 } = req.query;
    
    const patterns = await pythonBridge.callPythonFunction('identify_mood_patterns', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: patterns
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get activity-mood correlations
 */
exports.getActivityMoodCorrelations = async (req, res, next) => {
  try {
    const { days = 90 } = req.query;
    
    const correlations = await pythonBridge.callPythonFunction('identify_activity_mood_correlations', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: correlations
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get sleep-mood correlations
 */
exports.getSleepMoodCorrelations = async (req, res, next) => {
  try {
    const { days = 90 } = req.query;
    
    const correlations = await pythonBridge.callPythonFunction('identify_sleep_mood_correlations', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: correlations
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get comprehensive analysis
 */
exports.getComprehensiveAnalysis = async (req, res, next) => {
  try {
    const { days = 90 } = req.query;
    
    const analysis = await pythonBridge.callPythonFunction('generate_comprehensive_analysis', {
      days: parseInt(days, 10)
    });
    
    res.json({
      success: true,
      data: analysis
    });
  } catch (error) {
    next(error);
  }
};
