import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faSmile,
  faRunning,
  faBed,
  faChartLine,
  faLightbulb,
  faSpinner
} from '@fortawesome/free-solid-svg-icons';
import { useAppContext } from '../context/AppContext';
import MoodChart from './charts/MoodChart';
import ActivityChart from './charts/ActivityChart';
import SleepChart from './charts/SleepChart';
import InsightCard from './InsightCard';
import './Dashboard.css';

const Dashboard = () => {
  const {
    moodEntries,
    activityEntries,
    sleepEntries,
    moodPatterns,
    activityCorrelations,
    sleepCorrelations,
    loading,
    errors,
    fetchMoodEntries,
    fetchActivityEntries,
    fetchSleepEntries,
    runPatternAnalysis,
    runCorrelationAnalysis
  } = useAppContext();
  
  const [timeRange, setTimeRange] = useState(30); // Default to 30 days
  const [insights, setInsights] = useState([]);
  
  // Fetch data on component mount and when time range changes
  useEffect(() => {
    const fetchData = async () => {
      try {
        await Promise.all([
          fetchMoodEntries(timeRange),
          fetchActivityEntries(timeRange),
          fetchSleepEntries(timeRange)
        ]);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };
    
    fetchData();
  }, [timeRange, fetchMoodEntries, fetchActivityEntries, fetchSleepEntries]);
  
  // Run analysis when we have enough data
  useEffect(() => {
    const runAnalysis = async () => {
      if (moodEntries.length >= 5) {
        try {
          await Promise.all([
            runPatternAnalysis(90),
            runCorrelationAnalysis(90)
          ]);
        } catch (error) {
          console.error('Error running analysis:', error);
        }
      }
    };
    
    runAnalysis();
  }, [moodEntries.length, runPatternAnalysis, runCorrelationAnalysis]);
  
  // Generate insights based on analysis results
  useEffect(() => {
    const newInsights = [];
    
    // Add insights from mood patterns
    if (moodPatterns?.status === 'success') {
      newInsights.push(...(moodPatterns.insights || []));
    }
    
    // Add insights from activity correlations
    if (activityCorrelations?.status === 'success') {
      newInsights.push(...(activityCorrelations.insights || []));
    }
    
    // Add insights from sleep correlations
    if (sleepCorrelations?.status === 'success') {
      newInsights.push(...(sleepCorrelations.insights || []));
    }
    
    // Limit to top 5 insights
    setInsights(newInsights.slice(0, 5));
  }, [moodPatterns, activityCorrelations, sleepCorrelations]);
  
  // Calculate summary statistics
  const calculateStats = () => {
    if (!moodEntries.length) {
      return {
        averageMood: null,
        moodTrend: null,
        activityCount: 0,
        sleepAverage: null
      };
    }
    
    // Calculate average mood
    const moodLevels = moodEntries.map(entry => entry.mood_level);
    const averageMood = moodLevels.reduce((sum, level) => sum + level, 0) / moodLevels.length;
    
    // Calculate mood trend (comparing first half to second half)
    const halfIndex = Math.floor(moodEntries.length / 2);
    const firstHalf = moodEntries.slice(0, halfIndex);
    const secondHalf = moodEntries.slice(halfIndex);
    
    const firstHalfAvg = firstHalf.reduce((sum, entry) => sum + entry.mood_level, 0) / firstHalf.length;
    const secondHalfAvg = secondHalf.reduce((sum, entry) => sum + entry.mood_level, 0) / secondHalf.length;
    
    const moodTrend = secondHalfAvg - firstHalfAvg;
    
    // Calculate activity count
    const activityCount = activityEntries.length;
    
    // Calculate average sleep duration
    const sleepDurations = sleepEntries.map(entry => entry.duration_hours);
    const sleepAverage = sleepDurations.length
      ? sleepDurations.reduce((sum, duration) => sum + duration, 0) / sleepDurations.length
      : null;
    
    return {
      averageMood,
      moodTrend,
      activityCount,
      sleepAverage
    };
  };
  
  const stats = calculateStats();
  
  // Handle time range change
  const handleTimeRangeChange = (event) => {
    setTimeRange(parseInt(event.target.value, 10));
  };
  
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h3>Your Mental Health Overview</h3>
        <div className="time-range-selector">
          <label htmlFor="time-range">Time Range:</label>
          <select
            id="time-range"
            value={timeRange}
            onChange={handleTimeRangeChange}
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={180}>Last 6 months</option>
            <option value={365}>Last year</option>
          </select>
        </div>
      </div>
      
      <div className="dashboard-stats">
        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className="stat-icon mood">
            <FontAwesomeIcon icon={faSmile} />
          </div>
          <div className="stat-content">
            <h4>Average Mood</h4>
            {loading.moodEntries ? (
              <FontAwesomeIcon icon={faSpinner} spin />
            ) : (
              <p className="stat-value">{stats.averageMood ? stats.averageMood.toFixed(1) : 'N/A'}</p>
            )}
            {stats.moodTrend && (
              <p className={`stat-trend ${stats.moodTrend > 0 ? 'positive' : stats.moodTrend < 0 ? 'negative' : ''}`}>
                {stats.moodTrend > 0 ? '↑' : stats.moodTrend < 0 ? '↓' : '→'} {Math.abs(stats.moodTrend).toFixed(1)}
              </p>
            )}
          </div>
        </motion.div>
        
        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <div className="stat-icon activity">
            <FontAwesomeIcon icon={faRunning} />
          </div>
          <div className="stat-content">
            <h4>Activities</h4>
            {loading.activityEntries ? (
              <FontAwesomeIcon icon={faSpinner} spin />
            ) : (
              <p className="stat-value">{stats.activityCount}</p>
            )}
            <p className="stat-label">recorded</p>
          </div>
        </motion.div>
        
        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <div className="stat-icon sleep">
            <FontAwesomeIcon icon={faBed} />
          </div>
          <div className="stat-content">
            <h4>Avg. Sleep</h4>
            {loading.sleepEntries ? (
              <FontAwesomeIcon icon={faSpinner} spin />
            ) : (
              <p className="stat-value">{stats.sleepAverage ? `${stats.sleepAverage.toFixed(1)}h` : 'N/A'}</p>
            )}
            <p className="stat-label">per night</p>
          </div>
        </motion.div>
      </div>
      
      <div className="dashboard-charts">
        <motion.div
          className="chart-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.4 }}
        >
          <h4>Mood Timeline</h4>
          {loading.moodEntries ? (
            <div className="loading-indicator">
              <FontAwesomeIcon icon={faSpinner} spin />
              <p>Loading mood data...</p>
            </div>
          ) : moodEntries.length > 0 ? (
            <MoodChart data={moodEntries} />
          ) : (
            <p className="no-data-message">No mood data available. Start tracking your mood to see trends.</p>
          )}
        </motion.div>
        
        <div className="charts-row">
          <motion.div
            className="chart-container half"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.5 }}
          >
            <h4>Activity Impact</h4>
            {loading.activityEntries ? (
              <div className="loading-indicator">
                <FontAwesomeIcon icon={faSpinner} spin />
                <p>Loading activity data...</p>
              </div>
            ) : activityEntries.length > 0 ? (
              <ActivityChart data={activityEntries} />
            ) : (
              <p className="no-data-message">No activity data available. Record activities to see their impact.</p>
            )}
          </motion.div>
          
          <motion.div
            className="chart-container half"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.6 }}
          >
            <h4>Sleep Quality</h4>
            {loading.sleepEntries ? (
              <div className="loading-indicator">
                <FontAwesomeIcon icon={faSpinner} spin />
                <p>Loading sleep data...</p>
              </div>
            ) : sleepEntries.length > 0 ? (
              <SleepChart data={sleepEntries} />
            ) : (
              <p className="no-data-message">No sleep data available. Track your sleep to see patterns.</p>
            )}
          </motion.div>
        </div>
      </div>
      
      <motion.div
        className="dashboard-insights"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.7 }}
      >
        <div className="insights-header">
          <h4>
            <FontAwesomeIcon icon={faLightbulb} />
            Insights & Patterns
          </h4>
          {(loading.patterns || loading.correlations) && (
            <div className="loading-badge">
              <FontAwesomeIcon icon={faSpinner} spin />
              Analyzing...
            </div>
          )}
        </div>
        
        {insights.length > 0 ? (
          <div className="insights-list">
            {insights.map((insight, index) => (
              <InsightCard key={index} insight={insight} delay={index * 0.1} />
            ))}
          </div>
        ) : (
          <p className="no-data-message">
            {moodEntries.length < 5 ? (
              'Record at least 5 mood entries to generate insights.'
            ) : (
              'No insights available yet. Continue tracking to discover patterns.'
            )}
          </p>
        )}
      </motion.div>
    </div>
  );
};

export default Dashboard;
