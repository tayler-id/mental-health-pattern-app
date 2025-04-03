import React, { createContext, useState, useEffect, useContext } from 'react';
import { apiService } from '../services/apiService';

// Create context
const AppContext = createContext();

// Custom hook to use the context
export const useAppContext = () => useContext(AppContext);

// Provider component
export const AppProvider = ({ children }) => {
  // State for mood entries
  const [moodEntries, setMoodEntries] = useState([]);
  const [activityEntries, setActivityEntries] = useState([]);
  const [sleepEntries, setSleepEntries] = useState([]);
  
  // State for analysis results
  const [moodPatterns, setMoodPatterns] = useState(null);
  const [activityCorrelations, setActivityCorrelations] = useState(null);
  const [sleepCorrelations, setSleepCorrelations] = useState(null);
  
  // State for loading and errors
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});
  
  // State for user settings
  const [settings, setSettings] = useState({
    theme: 'light',
    dateFormat: 'MM/DD/YYYY',
    timeFormat: '12h',
    notificationsEnabled: true
  });
  
  // Function to fetch mood entries
  const fetchMoodEntries = async (days = 30) => {
    setLoading(prev => ({ ...prev, moodEntries: true }));
    setErrors(prev => ({ ...prev, moodEntries: null }));
    
    try {
      const response = await apiService.getMoodEntries(days);
      setMoodEntries(response.data);
    } catch (error) {
      console.error('Error fetching mood entries:', error);
      setErrors(prev => ({ ...prev, moodEntries: error.message }));
    } finally {
      setLoading(prev => ({ ...prev, moodEntries: false }));
    }
  };
  
  // Function to fetch activity entries
  const fetchActivityEntries = async (days = 30) => {
    setLoading(prev => ({ ...prev, activityEntries: true }));
    setErrors(prev => ({ ...prev, activityEntries: null }));
    
    try {
      const response = await apiService.getActivityEntries(days);
      setActivityEntries(response.data);
    } catch (error) {
      console.error('Error fetching activity entries:', error);
      setErrors(prev => ({ ...prev, activityEntries: error.message }));
    } finally {
      setLoading(prev => ({ ...prev, activityEntries: false }));
    }
  };
  
  // Function to fetch sleep entries
  const fetchSleepEntries = async (days = 30) => {
    setLoading(prev => ({ ...prev, sleepEntries: true }));
    setErrors(prev => ({ ...prev, sleepEntries: null }));
    
    try {
      const response = await apiService.getSleepEntries(days);
      setSleepEntries(response.data);
    } catch (error) {
      console.error('Error fetching sleep entries:', error);
      setErrors(prev => ({ ...prev, sleepEntries: error.message }));
    } finally {
      setLoading(prev => ({ ...prev, sleepEntries: false }));
    }
  };
  
  // Function to create a mood entry
  const createMoodEntry = async (moodData) => {
    setLoading(prev => ({ ...prev, createMood: true }));
    setErrors(prev => ({ ...prev, createMood: null }));
    
    try {
      const response = await apiService.createMoodEntry(moodData);
      setMoodEntries(prev => [...prev, response.data]);
      return response.data;
    } catch (error) {
      console.error('Error creating mood entry:', error);
      setErrors(prev => ({ ...prev, createMood: error.message }));
      throw error;
    } finally {
      setLoading(prev => ({ ...prev, createMood: false }));
    }
  };
  
  // Function to create an activity entry
  const createActivityEntry = async (activityData) => {
    setLoading(prev => ({ ...prev, createActivity: true }));
    setErrors(prev => ({ ...prev, createActivity: null }));
    
    try {
      const response = await apiService.createActivityEntry(activityData);
      setActivityEntries(prev => [...prev, response.data]);
      return response.data;
    } catch (error) {
      console.error('Error creating activity entry:', error);
      setErrors(prev => ({ ...prev, createActivity: error.message }));
      throw error;
    } finally {
      setLoading(prev => ({ ...prev, createActivity: false }));
    }
  };
  
  // Function to create a sleep entry
  const createSleepEntry = async (sleepData) => {
    setLoading(prev => ({ ...prev, createSleep: true }));
    setErrors(prev => ({ ...prev, createSleep: null }));
    
    try {
      const response = await apiService.createSleepEntry(sleepData);
      setSleepEntries(prev => [...prev, response.data]);
      return response.data;
    } catch (error) {
      console.error('Error creating sleep entry:', error);
      setErrors(prev => ({ ...prev, createSleep: error.message }));
      throw error;
    } finally {
      setLoading(prev => ({ ...prev, createSleep: false }));
    }
  };
  
  // Function to run pattern analysis
  const runPatternAnalysis = async (days = 90) => {
    setLoading(prev => ({ ...prev, patterns: true }));
    setErrors(prev => ({ ...prev, patterns: null }));
    
    try {
      const response = await apiService.runPatternRecognition(days);
      setMoodPatterns(response.data);
      return response.data;
    } catch (error) {
      console.error('Error running pattern analysis:', error);
      setErrors(prev => ({ ...prev, patterns: error.message }));
      throw error;
    } finally {
      setLoading(prev => ({ ...prev, patterns: false }));
    }
  };
  
  // Function to run correlation analysis
  const runCorrelationAnalysis = async (days = 90) => {
    setLoading(prev => ({ ...prev, correlations: true }));
    setErrors(prev => ({ ...prev, correlations: null }));
    
    try {
      const activityResponse = await apiService.getActivityMoodCorrelations(days);
      const sleepResponse = await apiService.getSleepMoodCorrelations(days);
      
      setActivityCorrelations(activityResponse.data);
      setSleepCorrelations(sleepResponse.data);
      
      return {
        activity: activityResponse.data,
        sleep: sleepResponse.data
      };
    } catch (error) {
      console.error('Error running correlation analysis:', error);
      setErrors(prev => ({ ...prev, correlations: error.message }));
      throw error;
    } finally {
      setLoading(prev => ({ ...prev, correlations: false }));
    }
  };
  
  // Function to update settings
  const updateSettings = (newSettings) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
    // In a real app, you might want to save these to localStorage or a backend
    localStorage.setItem('appSettings', JSON.stringify({ ...settings, ...newSettings }));
  };
  
  // Load settings from localStorage on initial render
  useEffect(() => {
    const savedSettings = localStorage.getItem('appSettings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (error) {
        console.error('Error parsing saved settings:', error);
      }
    }
  }, []);
  
  // Value object to be provided to consumers
  const value = {
    // Data
    moodEntries,
    activityEntries,
    sleepEntries,
    moodPatterns,
    activityCorrelations,
    sleepCorrelations,
    settings,
    
    // Loading and error states
    loading,
    errors,
    
    // Functions
    fetchMoodEntries,
    fetchActivityEntries,
    fetchSleepEntries,
    createMoodEntry,
    createActivityEntry,
    createSleepEntry,
    runPatternAnalysis,
    runCorrelationAnalysis,
    updateSettings
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};
